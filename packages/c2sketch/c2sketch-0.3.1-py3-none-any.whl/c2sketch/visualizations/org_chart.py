from __future__ import annotations
from ..models import *
from dataclasses import dataclass, field
from itertools import batched

__all__ = [
    'svg_org_chart'
]

MARGIN_VERTICAL = 5
MARGIN_HORIZONTAL = 5
DIAGRAM_MARGIN = 100
MAX_COLUMNS = 3
FONT = 'Barlow'

def svg_org_chart(models: ModelSet, model_id: ModelID) -> str:
   
    #Layout strategy
    # - first show individuals in a grid with multiple rows
    # - below show organisations all as full width boxes (with some margin)
    #   all below each other


    #Index organization members
    member_index: dict[ActorID,set[ActorID]] = {}
    group_index: dict[ActorID,set[ActorID]] = {}
    actor_index: dict[ActorID,Actor] = {}

    for actor in (models.get_actor_by_id(id) for id in models.list_actors(model_id)):
        node_id = actor.node_id
        actor_index[node_id] = actor

        if node_id not in member_index:
            member_index[node_id] = set()
        if node_id not in group_index:
            group_index[node_id] = set()
        for member in actor.members:
            member_index[node_id].add(member)
            if member not in group_index:
                group_index[member] = set()
            group_index[member].add(node_id)
                
        for group in actor.groups:
            group_index[node_id].add(group)
            if group not in member_index:
                member_index[group] = set()
            member_index[group].add(node_id)

    #Generate nested boxes from the index
    @dataclass
    class IndividualBox:
        model: Actor

        @property
        def width(self):
            return 150
        
        @property
        def height(self):
            return 30
        
        def render(self, x_offset = 0, y_offset = 0) -> str:
            color = 'white'
            box_shape =  f'<rect x="{x_offset}" y="{y_offset}" width="{self.width}" height="{self.height}" fill="{color}" stroke="black" rx="5" />'
            box_text = f'<text text-anchor="middle" font-family="{FONT}" font-size="12" x="{x_offset + 75}" y="{y_offset + 20}">{self.model.label}</text>'

            return box_shape + box_text

    @dataclass
    class OrganizationBox:
        model: Actor
        individuals: list[IndividualBox] = field(default_factory=list)
        organizations: list[OrganizationBox] = field(default_factory=list)
       
        @property
        def width(self):
            individuals_width = max(sum(i.width for i in row) for row in batched(self.individuals,MAX_COLUMNS)) \
                + ((min(len(self.individuals),MAX_COLUMNS) + 1) * MARGIN_HORIZONTAL) if self.individuals else 0 if self.individuals else 0
            
            organizations_width = max(o.width for o in self.organizations) if self.organizations else 0
            return max(individuals_width,organizations_width)

        @property
        def height(self):
            title_height = 30
            individuals_height = sum((max(i.height for i in row)) for row in batched(self.individuals,MAX_COLUMNS)) if self.individuals else 0
            individuals_height = sum((max(i.height for i in row)) for row in batched(self.individuals,MAX_COLUMNS)) \
                + (len(self.individuals) // MAX_COLUMNS + 2) * MARGIN_VERTICAL if self.individuals else 0
           
            organizations_height = sum(o.height for o in self.organizations) if self.organizations else 0
            
            return title_height + individuals_height + organizations_height
          
        def render(self, x_offset = 0, y_offset = 0):
            color = 'transparent'
            
            #Create box and title
            box_shape =  f'<rect x="{x_offset}" y="{y_offset}" width="{self.width}" height="{self.height}" fill="{color}" stroke="black" rx="5" />'
            
            title_frame = f'<rect x="{x_offset}" y="{y_offset}" width="{self.width}" height="30" fill="black" rx="5" />'
            title_text = f'<text text-anchor="middle" font-family="{FONT}" font-size="12" x="{x_offset + self.width // 2}" y="{y_offset + 15}" fill="white" >{self.model.label}</text>'
            
            box_children = []
            iy_offset = y_offset + 30

            if self.individuals:
                iy_offset += MARGIN_VERTICAL
                for row in batched(self.individuals,MAX_COLUMNS):
                    ix_offset = x_offset + MARGIN_HORIZONTAL
                    for child_box in row:
                        box_children.append(child_box.render(ix_offset,iy_offset))
                        ix_offset += child_box.width + MARGIN_HORIZONTAL
                    iy_offset += max(i.height for i in row) + MARGIN_VERTICAL
            
            if self.organizations:
                for child_box in self.organizations:
                    box_children.append(child_box.render(x_offset,iy_offset))
                    iy_offset += child_box.height

            return box_shape + title_frame + title_text + ''.join(box_children)

    @dataclass
    class ModelBox:
        model: Model
        individuals: list[IndividualBox] = field(default_factory=list)
        organizations: list[OrganizationBox] = field(default_factory=list)
    
        @property
        def width(self):
            individuals_width = max(sum(i.width for i in row) for row in batched(self.individuals,MAX_COLUMNS)) \
                + ((min(len(self.individuals),MAX_COLUMNS) - 1) * MARGIN_HORIZONTAL) if self.individuals else 0 if self.individuals else 0 
            organizations_width = max(o.width for o in self.organizations) if self.organizations else 0
            return max(individuals_width,organizations_width)

        @property
        def height(self):
            title_height = 50
            individuals_height = sum((max(i.height for i in row)) for row in batched(self.individuals,MAX_COLUMNS)) \
                + (len(self.individuals) // MAX_COLUMNS) * MARGIN_VERTICAL if self.individuals else 0
           
            organizations_height = sum(o.height for o in self.organizations) + ((len(self.organizations) -1) * MARGIN_VERTICAL) if self.organizations else 0

            return title_height + individuals_height + organizations_height + (MARGIN_VERTICAL if self.individuals and self.organizations else 0)
        
        def render(self, x_offset = 0, y_offset = 0):
            box_children = []
            
            title_text = f'<text x="{x_offset + self.width // 2}" y="{y_offset}" font-family="Barlow" text-anchor="middle" font-weight="bold" font-size="30">{self.model.label}</text>'
            y_offset += 50
            if self.individuals:
                for row in batched(self.individuals,MAX_COLUMNS):
                    xi_offset = x_offset
                    for child_box in row:
                        box_children.append(child_box.render(xi_offset,y_offset))
                        xi_offset += child_box.width + MARGIN_HORIZONTAL
                    y_offset += max(i.height for i in row) + MARGIN_VERTICAL
            
            if self.organizations:
                for child_box in self.organizations:
                    box_children.append(child_box.render(x_offset,y_offset))
                    y_offset += child_box.height + MARGIN_VERTICAL

            return title_text + ''.join(box_children)


    def to_box(actor_id: ActorID) -> IndividualBox | OrganizationBox:
        if member_index[actor_id]:
            box = OrganizationBox(actor_index[actor_id],[])
            for member_id in member_index[actor_id]:
                if member_id not in member_index:
                    continue
                member_box = to_box(member_id)
                if isinstance(member_box,IndividualBox):
                    box.individuals.append(member_box)
                else:
                    box.organizations.append(member_box)
            return box
        else:
            return IndividualBox(actor_index[actor_id])
        
    model_box = ModelBox(models.get_model_by_id(model_id))
    for actor_id in sorted(actor_index.keys()):
        if actor_id not in member_index:
            continue
        actor_box = to_box(actor_id)
        
        if isinstance(actor_box,OrganizationBox):
            model_box.organizations.append(actor_box)
        else:
            #Only add individuals that are not part of any groups
            if not group_index[actor_id]:
                model_box.individuals.append(actor_box)
  
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{model_box.width + 2 * DIAGRAM_MARGIN}" height="{model_box.height + 2 * DIAGRAM_MARGIN}">{model_box.render(DIAGRAM_MARGIN,DIAGRAM_MARGIN)}</svg>'
