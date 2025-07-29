from __future__ import annotations

from ..models import *
from .color_util import black_or_white
from dataclasses import dataclass, field
from itertools import groupby
from enum import Enum
from xml.sax.saxutils import escape
import math

__all__ = [
    'svg_task_hierarchy'
]

BOX_WIDTH = 100
BOX_HEIGHT = 60
BOX_MARGIN_VERTICAL = 40
BOX_MARGIN_HORIZONTAL = 20
DIAGRAM_MARGIN = 100
FONT = 'Barlow'

def svg_task_hierarchy(models: ModelSet, model_id: ModelID) -> str:
    model_node = models.get_model_by_id(model_id)

    @dataclass
    class TaskBox:
        model_node: Model | TaskNode
        parent: TaskBox | None
        sub_tasks: list[TaskBox]
        number: str

        def __eq__(self, other): #Only used for finding an index in a list, no need to compare attributes
            return self is other

    #TODO: Generalize to Positioned[T] type, but tricky because of the tree-structure
    #      That will probably mean a generalized tree too
    @dataclass
    class PositionedTaskBox:
        model_node: Model | TaskNode
        parent: PositionedTaskBox | None
        sub_tasks: list[PositionedTaskBox]
        number: str
        
        x_position: int # Horizontal position on a grid
        y_position: int # Vertical position on a grid

        def __eq__(self, other): #Only used for finding an index in a list, no need to compare attributes
            return self is other

    @dataclass
    class InfoSpaceBox:
        model_node: InformationSpace
        used_by: list[tuple[TaskNode,bool,bool]] = field(default_factory=list)
        triggers: list[TaskNode] = field(default_factory=list)

    @dataclass
    class PositionedInfoSpaceBox:
        model_node: InformationSpace
        used_by: list[tuple[PositionedTaskBox,bool,bool]]
        triggers: list[PositionedTaskBox]

        x_position: int # Horizontal position on a grid
        y_position: int # Vertical position on a grid

    class Side(Enum):
        left = 0
        right = 1

    # EXTRACTING THE SHAPE OF THE TREE
    def model_node_to_boxes(node: Model | TaskNode, parent: TaskBox | None = None, known_info_boxes: list[InfoSpaceBox] | None = None, number_prefix = '') -> tuple[TaskBox,list[InfoSpaceBox]]:                                                                                                                                                                     
        
        if known_info_boxes is None:
            known_info_boxes = []

        sub_nodes = [sub_node for sub_node in node.complete_nodes if isinstance(sub_node,TaskNode)]
        
        result_tree = TaskBox(
            model_node = node,
            parent = parent,
            sub_tasks = [],
            number = number_prefix
        )
        result_info_boxes = []
        
        #Group TaskInstance nodes together with their TaskDefinition node
        def group_task_instances(nodes):
            i = 0
            for i in range(len(nodes)):
                if isinstance(nodes[i],TaskInstance):
                    j = i
                    #Move the node left until its left sibling is either its definition or another instance of the same definition
                    while j > 0 and not ((isinstance(nodes[j-1],TaskInstance) or isinstance(nodes[j-1],TaskDefinition)) and nodes[j].name == nodes[j-1].name):
                        nodes[j-1], nodes[j] = nodes[j], nodes[j-1]
                        j -= 1                    

        group_task_instances(sub_nodes)

        if sub_nodes:
            number = 0
            for sub_node in sub_nodes:
                if not (isinstance(sub_node,TaskInstance) or isinstance(sub_node,ImplicitTaskInstance)):
                    number += 1
                    number_str = str(number)
                else:
                    number_str = f'{number}-{sub_node.sequence}'
                sub_number = f'{number_prefix}.{number_str}' if number_prefix != '' else number_str

                sub_tree, sub_info_boxes = model_node_to_boxes(sub_node,result_tree,known_info_boxes,sub_number)
                result_tree.sub_tasks.append(sub_tree)
                result_info_boxes.extend(sub_info_boxes)
                
        elif isinstance(node,TaskNode):
            
            if isinstance(node,Task) or isinstance(node,TaskDefinition):
                info_reqs = node.info_space_requirements
            elif isinstance(node,TaskInstance):
                info_reqs = node.get_definition().info_space_requirements
            elif isinstance(node,ImplicitTask):
                info_reqs = node.template.info_space_requirements
            elif isinstance(node,ImplicitTaskInstance):
                info_reqs = node.template.get_definition().info_space_requirements
            else:
                info_reqs = []
            
            info_bindings = resolve_info_space_bindings(models, node)
            for info_req in info_reqs:
                _, info_space = info_bindings[info_req.name]
                if info_space is not None:
                    info_box_exists = False
                    for info_box in known_info_boxes:
                        if info_space is info_box.model_node:
                            info_box.used_by.append((node,info_req.read,info_req.write))
                            info_box_exists = True
                            break
                    if not info_box_exists:
                        info_box = InfoSpaceBox(model_node=info_space,used_by=[(node,info_req.read,info_req.write)],triggers=[])
                        result_info_boxes.append(info_box)
                        known_info_boxes.append(info_box)
    
            for _, info_space in resolve_trigger_bindings(models,node):
                if info_space is None:
                    continue

                info_box_exists = False
                for info_box in known_info_boxes:
                    if info_space is info_box.model_node:
                        info_box.triggers.append(node)
                        info_box_exists = True
                        break
                    if not info_box_exists:
                        info_box = InfoSpaceBox(model_node=info_space,used_by=[],triggers=[node])
                        result_info_boxes.append(info_box)
                        known_info_boxes.append(info_box)
               
        return (result_tree,result_info_boxes)

    # POSITIONING THE NODES

    def position_tree(tree: TaskBox) -> PositionedTaskBox:
        positioned_tree = position_nodes(tree,None)
        center_nodes(positioned_tree, None, [], [])
        return positioned_tree

    def position_nodes(node: TaskBox, parent: PositionedTaskBox | None, layer: int = 0) -> PositionedTaskBox:
        
        positioned_node = PositionedTaskBox(
            model_node = node.model_node,
            parent = parent,
            sub_tasks = [],
            number = node.number,
            #Root of the tree is always position 0
            x_position = 0,
            y_position = layer
        )
        
        #Position children one by one
        for i, child in enumerate(node.sub_tasks):
            #First child is simply placed below the root
            positioned_child = position_nodes(child, positioned_node, layer + 1)

            #Try to create as much space as possible
            push(positioned_child,[],Side.right)
            
            if i > 0: #Remaining children are shifted right to not overlap with left sibling
                
                current_edge = edge_of(positioned_node.sub_tasks[0:i],Side.right)
                addition_edge= edge_of([positioned_child],Side.left)
                edge_differences = [l - r for l, r in zip(current_edge,addition_edge)]
                if edge_differences:
                    child_shift = 1 + max(edge_differences)
                else:
                    child_shift = 1
                shift(positioned_child,child_shift)

            positioned_node.sub_tasks.append(positioned_child)
       
            #Shift everything left after adding the child branch
            #to prepare for adding the next branch
            push(positioned_node,[],Side.left)
        return positioned_node
    
    def shift(node: PositionedTaskBox, amount: int):
        """Adjust the position of all nodes in a subtree by the same amount"""
        node.x_position = amount if node.x_position is None else node.x_position + amount
        for child in node.sub_tasks:
            shift(child,amount)

    def push(node: PositionedTaskBox, boundary: list[int], side: Side):
        """Shift all children as much to one side as possible without crossing a boundary"""

        if not node.sub_tasks:
            return
        
        opposite_side = Side.right if side is Side.left else Side.left

        # Shift all children such that the first child aligns with this node
        shift_child = node.sub_tasks[-1 if side is Side.left else 0]
        shift_amount = node.x_position - shift_child.x_position
        
        # When pushing left, shift_amount is negative or zero.
        # When pushing right, shift_amount is positive or zero

        # When pushing left, the indices in the border are all smaller than this node's left edge
        # When pushing right, the indices in the border are alll bigger than this node's right edge
        
        edge = edge_of([node],side)
        for boundary_position, edge_position in list(zip(boundary,edge))[1:]:
            if side is Side.left:
                allowed_shift = (boundary_position + 1) - edge_position
                shift_amount = max(shift_amount, allowed_shift)
            else:
                allowed_shift = (boundary_position - 1) - edge_position
                shift_amount = min(shift_amount, allowed_shift)

        # Move all children together
        for child in node.sub_tasks:
            shift(child,shift_amount)
        
        # The order in which we recursively process children
        # Is the same as the direction to where we are pushing the nodes
        child_indices = range(len(node.sub_tasks)) if side is Side.left else range(len(node.sub_tasks) -1, -1,-1)
        start_i = child_indices[0]
        
        for i in child_indices:
            if i == start_i:
                child_boundary = boundary[1:]
            else:
                child_boundary = edge_of(node.sub_tasks[start_i : i : 1 if side is Side.left else -1], opposite_side)
                #Make sure we cover the full length of the border
                #Even if the siblings are not as deep
                if len(child_boundary) < (len(boundary) - 1):
                    child_boundary = child_boundary + boundary[1 + len(child_boundary):]

            push(node.sub_tasks[i], child_boundary, side)

    def edge_of(nodes: list[PositionedTaskBox], side: Side) -> list[int]:
        """Find the positions of the outermost nodes on a specific side for a set of adjacent nodes."""

        def merge_edges(edges: list[list[int]]) -> list[int]:
        
            current_candidates = [edge[0] for edge in edges if len(edge) > 0]
            if len(current_candidates) == 0:
                return []
            elif len(current_candidates) == 1:
                current = current_candidates[0]
            else:
                current = min(current_candidates) if side is Side.left else max(current_candidates)
            return [current] + merge_edges([e[1:] for e in edges])
            
        edges = [[node.x_position] + edge_of(node.sub_tasks,side) for node in nodes]
        
        return merge_edges(edges)

    def center_nodes(node: PositionedTaskBox, parent: PositionedTaskBox | None, left_boundary: list[int], right_boundary: list[int]) -> None:
        """Center nodes above their children without crossing the given boundaries."""

        if not node.sub_tasks:
            return
    
        # First center children
        for i in range(len(node.sub_tasks)):
            if i == 0:
                child_left_boundary = left_boundary[1:]
            else:
                child_left_boundary = edge_of(node.sub_tasks[:i],Side.right)
                child_left_boundary = child_left_boundary + left_boundary[1+len(child_left_boundary):]
            if i == len(node.sub_tasks) - 1:
                child_right_boundary = right_boundary[1:]
            else:
                child_right_boundary = edge_of(node.sub_tasks[i+1:],Side.left)
                child_right_boundary = child_right_boundary + right_boundary[1+len(child_right_boundary):]

            center_nodes(node.sub_tasks[i],node,child_left_boundary,child_right_boundary)

        # We can't center nodes who are the single child of their parent
        if not parent is None and len(parent.sub_tasks) == 1:
            return
        # Try to put in the center of its children
        max_child_pos = max(child.x_position for child in node.sub_tasks)
        min_child_pos = min(child.x_position for child in node.sub_tasks)
        center_position = min_child_pos + (max_child_pos - min_child_pos) // 2

        if left_boundary:
            center_position = max(center_position,left_boundary[0] + 1)
        if right_boundary:
            center_position = min(center_position,right_boundary[0] - 1)
            
        node.x_position = center_position

    def position_info_boxes(info_boxes: list[InfoSpaceBox], tree: PositionedTaskBox) -> list[PositionedInfoSpaceBox]:

        #Not very efficient...
        def find_task_boxes(task_use: list[tuple[TaskNode,bool,bool]], node: PositionedTaskBox) -> list[tuple[PositionedTaskBox,bool,bool]]:
            
            result = []
            #Check current node
            if isinstance(node.model_node,TaskNode):
                for model, read, write in task_use:
                    if node.model_node is model:
                        result.append((node,read,write))
            for sub_task in node.sub_tasks:
                result.extend(find_task_boxes(task_use,sub_task))

            return result

        def find_tree_positions(node: PositionedTaskBox):
            positions = [(node.x_position,node.y_position)]
            for sub_task in node.sub_tasks:
                positions.extend(find_tree_positions(sub_task))
            return positions
        
        tree_positions = find_tree_positions(tree)
        
        #Set initial positions
        positioned_info_boxes = []
        for box in info_boxes:
            used_by = find_task_boxes(box.used_by,tree)
            triggers = [b for b,_,_ in find_task_boxes([(t,True,True) for t in box.triggers],tree)] #Bit of a hack
            relevant_boxes = [b for b,_,_ in used_by] + triggers

            x_position = sum(p.x_position for p in relevant_boxes) // len(relevant_boxes)
            x_width = max(p.x_position for p in relevant_boxes) - min(p.x_position for p in relevant_boxes)
            y_position = max(p.y_position for p in relevant_boxes) + max(1,x_width // 6)
            positioned_info_boxes.append(
                PositionedInfoSpaceBox(
                    box.model_node,
                    used_by,
                    triggers,
                    x_position,
                    y_position
                )
            )
        
        if positioned_info_boxes:
            def fix_horizontal(info_boxes: list[PositionedInfoSpaceBox]):
                #Remove horizontal overlap
                info_boxes = sorted(info_boxes,key = lambda box: box.x_position if box.x_position is not None else 0)
                #Remove overlap only when the vertical position is equal
                for layer in [list(layer) for _,layer in groupby(info_boxes, key = lambda box:box.y_position)]:
                    if len(layer) > 1:
                        middle = len(layer) // 2
                        #First half, move duplicate positions left 
                        for i in range(middle - 1, -1, -1):
                            layer_i = layer[i]
                            if layer_i.x_position is not None and layer_i.x_position == layer[i + 1].x_position:
                                layer_i.x_position -= 1
                        #Second half, move duplicate positions right
                        for i in range(middle, len(layer)):
                            layer_i = layer[i]
                            if layer_i.x_position is not None and layer_i.x_position == layer[i - 1].x_position:
                                layer_i.x_position += 1
                return info_boxes
            
            def fix_vertical(info_boxes: list[PositionedInfoSpaceBox], tree_positions):
                ok = True
                for box in info_boxes:
                    if (box.x_position,box.y_position) in tree_positions:
                        ok = False
                        while (box.x_position,box.y_position) in tree_positions:
                            if box.y_position is not None:
                                box.y_position += 1
                        
                return ok
            
            done = False
            while not done:
                #First fix horizonal overlap
                fix_horizontal(positioned_info_boxes)
                #Check vertical overlap and readjust horizontal if necessary
                #Changing vertical position may require fixing horizontal overlap on the lower layer
                done = fix_vertical(positioned_info_boxes,tree_positions)
          
        return positioned_info_boxes
    # RENDERING TO SVG
    
    def task_box_to_svg(box: PositionedTaskBox, x_offset = 0, y_offset = 0) -> str:

        left_x = box.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + x_offset
        top_y = box.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + y_offset
        
        center_x = left_x + (BOX_WIDTH // 2)
        center_y = top_y + (BOX_HEIGHT // 2)

        dash = '' if isinstance(box.model_node,Model) or box.model_node.is_concrete() else 'stroke-dasharray="4"'
        
        #Show implicit tasks with rounded corners
        # Only show concrete tasks with solid outlines, task definitions
        # define potential tasks, but are not tasks yet
        def is_implicit(node):
            return isinstance(node,ImplicitTask) or isinstance(node,ImplicitTaskDefinition) or isinstance(node,ImplicitTaskInstance)

        rx = 10 if is_implicit(box.model_node) else 0

        color = 'white'
        text_color = 'black'
        if isinstance(box.model_node,Task) or \
           isinstance(box.model_node,TaskDefinition) or \
           isinstance(box.model_node,TaskInstance):
           
            actor_constraints = resolve_task_actor_constraints(box.model_node)
            if actor_constraints:
                colors = []
                for actor_id in actor_constraints:
                    if models.actor_exists(actor_id,model_node.id):
                        actor = models.get_actor_by_id(actor_id, model_node.id)
                        if actor.color is not None:
                            colors.append(actor.color)
                if colors:
                    color = colors[0]
                    text_color = black_or_white(color)

        shapes = []
        if (isinstance(box.model_node,TaskDefinition) or isinstance(box.model_node,ImplicitTaskDefinition)) and not box.parent is None:
        
            shapes.append(
                f'<rect x="{left_x + 5}" y="{top_y - 5}" width="{BOX_WIDTH}" height="{BOX_HEIGHT}" fill="{color}" stroke="black" rx="{rx}" {dash} />', 
            )
            num_instances = len(box.model_node.get_instances())
            end_child = box.parent.sub_tasks[box.parent.sub_tasks.index(box) + num_instances]
            end_position = 0 if end_child.x_position is None else end_child.x_position
            start_x = center_x
            end_x = end_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            shapes.append(
                f'<line x1="{start_x}" y1="{center_y}" x2="{end_x}" y2="{center_y}" stroke="gray" stroke-dasharray="5 10" stroke-width="30" />'
            )

        label = box.model_node.label
        number = box.number
        if isinstance(box.model_node,Model):
            shapes.append(f'<text x="{center_x}" y="{center_y}" font-family="{FONT}" text-anchor="middle" font-weight="bold" font-size="30">{escape(box.model_node.label)}</text>')
        else:
            shapes.extend([
                f'<rect x="{left_x}" y="{top_y}" width="{BOX_WIDTH}" height="{BOX_HEIGHT}" fill="{color}" stroke="black" {dash} rx="{rx}" />',
                f'<text x="{center_x}" y="{center_y-14}" font-family="{FONT}" font-size="12" text-anchor="middle" fill="{text_color}">{number}</text>',
                f'<text x="{center_x}" y="{center_y}" font-family="{FONT}" font-size="12" text-anchor="middle" fill="{text_color}">{textwrap(center_x,label)}</text>'
            ])
        return '\n'.join(shapes)

    def info_box_edges_to_svg(box: PositionedInfoSpaceBox, x_offset = 0, y_offset = 0) -> str:
    
        shapes = []
        color = box.model_node.color if box.model_node.color is not None else '#999999'
        for task_box, read, write in box.used_by:
            #Draw the connections, the nodes will be drawn later
            start_x = task_box.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            start_y = task_box.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + BOX_HEIGHT + y_offset
            
            end_x = box.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            end_y = box.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + y_offset
            
            dash = '' if isinstance(task_box.model_node,TaskNode) and task_box.model_node.is_concrete() else 'stroke-dasharray="4"'
            shapes.append( f'<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="{color}" {dash} />')
        
            angle = math.atan2(end_y - start_y, end_x - start_x)

            if read:
                shapes.append(svg_triangle(start_x,start_y, math.pi * 0.5 + angle,color))
            if write:
                shapes.append(svg_triangle(end_x,end_y, math.pi * 1.5 + angle,color))

        for task_box in box.triggers:
            start_x = task_box.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            start_y = task_box.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + BOX_HEIGHT + y_offset
            
            end_x = box.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            end_y = box.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + y_offset
            shapes.append( f'<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="{color}" stroke-dasharray="10" />')
            angle = math.atan2(end_y - start_y, end_x - start_x)
            shapes.append(svg_triangle(start_x,start_y, math.pi * 0.5 + angle,color,False))
            
        return '\n'.join(shapes)
    
    def info_box_to_svg(box: PositionedInfoSpaceBox, x_offset = 0, y_offset = 0) -> str:
    
        top_y = box.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + y_offset
        left_x = box.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + x_offset
        center_x = left_x + (BOX_WIDTH // 2)
        center_y = top_y + (BOX_HEIGHT // 2)

        color = box.model_node.color if box.model_node.color is not None else 'white'
        text_color = black_or_white(box.model_node.color) if box.model_node.color is not None else 'black'
        shapes = []
        
        shapes.extend([
            f'<ellipse cx="{center_x}" cy="{center_y}" rx="{BOX_WIDTH//2}" ry="{BOX_HEIGHT//2}" fill="{color}" stroke="black" />',
            f'<text x="{center_x}" y="{center_y}" font-family="{FONT}" font-size="12" text-anchor="middle" fill="{text_color}">{textwrap(center_x,box.model_node.label)}</text>'
        ])
        return '\n'.join(shapes)
    
    def node_to_svg(tree: PositionedTaskBox, x_offset = 0, y_offset = 0) -> str:

        shapes = []
        shapes.append(task_box_to_svg(tree, x_offset, y_offset))
        
        if tree.sub_tasks:
            #Recursively draw children
            for child in tree.sub_tasks:
                shapes.append(node_to_svg(child, x_offset, y_offset))
            
            #Draw connecting lines
            y_position = tree.y_position * (BOX_HEIGHT + BOX_MARGIN_VERTICAL) + y_offset

            first_child_pos = tree.sub_tasks[0].x_position
            last_child_pos = tree.sub_tasks[-1].x_position
            start_x = first_child_pos * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            end_x = last_child_pos * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) + (BOX_WIDTH // 2) + x_offset
            y = y_position + BOX_HEIGHT + (BOX_MARGIN_VERTICAL // 2)

            shapes.append( f'<line x1="{start_x}" y1="{y}" x2="{end_x}" y2="{y}" stroke="black" />')
            
            start_y = y_position + BOX_HEIGHT 
            end_y = y_position + BOX_HEIGHT + (BOX_MARGIN_VERTICAL // 2)
            x = tree.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) \
                + (BOX_WIDTH // 2) + x_offset
            shapes.append( f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{end_y}" stroke="black" />')
            
            start_y = y_position + BOX_HEIGHT + (BOX_MARGIN_VERTICAL // 2)
            end_y = y_position + BOX_HEIGHT + BOX_MARGIN_VERTICAL
            for child in tree.sub_tasks:
                x = child.x_position * (BOX_WIDTH + BOX_MARGIN_HORIZONTAL) \
                    + (BOX_WIDTH // 2) + x_offset
                shapes.append( f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{end_y}" stroke="black" />')
                shapes.append(svg_triangle(x,end_y))
             
        return '\n'.join(shapes)

    def tree_dimension(tree: PositionedTaskBox) -> tuple[int,int]:
        
        max_x = max(edge_of([tree],Side.right)) + 1
        
        def depth(tree: PositionedTaskBox) -> int:
            if tree.sub_tasks:
                return max(depth(child) for child in tree.sub_tasks)
            else:
                return tree.y_position

        max_y = depth(tree)
        return (max_x,max_y)

    def info_box_depth(info_boxes: list[PositionedInfoSpaceBox]) -> int:
        return max(box.y_position for box in info_boxes) if info_boxes else 0

    def graph_to_svg(tree: PositionedTaskBox, info_boxes: list[PositionedInfoSpaceBox]) -> str:

        #Align the tree, and info boxes with the left border
        left_border = min(edge_of([tree],Side.left))
        if info_boxes:
            left_border = min(left_border,min(info_box.x_position for info_box in info_boxes if info_box.x_position is not None))
        shift(tree, 0 - left_border)
        
        for info_box in info_boxes:
            info_box.x_position -= left_border

        max_x, max_y = tree_dimension(tree)
        max_y = max(max_y,info_box_depth(info_boxes))

        width = (max_x * BOX_MARGIN_HORIZONTAL) + (max_x + 1) * BOX_WIDTH + (2 * DIAGRAM_MARGIN)
        height = (max_y * BOX_MARGIN_VERTICAL) + ((max_y + 1) * BOX_HEIGHT) + (2 * DIAGRAM_MARGIN)

        tree_svg = node_to_svg(tree,x_offset = DIAGRAM_MARGIN, y_offset= DIAGRAM_MARGIN)
        
        info_box_svg =  '\n'.join(info_box_to_svg(info_space, x_offset = DIAGRAM_MARGIN, y_offset= DIAGRAM_MARGIN) for info_space in info_boxes)
        info_box_edges_svg = '\n'.join(info_box_edges_to_svg(info_space, x_offset = DIAGRAM_MARGIN, y_offset= DIAGRAM_MARGIN) for info_space in info_boxes)
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n{info_box_edges_svg}\n{tree_svg}\n{info_box_svg}\n</svg>'

    task_tree, info_boxes = model_node_to_boxes(model_node)
    
    positioned_tree = position_tree(task_tree)
    positioned_info_boxes = position_info_boxes(info_boxes, positioned_tree)

    return graph_to_svg(positioned_tree, positioned_info_boxes)


#SVG Util
def svg_triangle(x,y, angle: float = 0.0, color = 'black',fill=True) -> str:

    sin_angle = math.sin(angle)
    cos_angle = math.cos(angle)

    x1, y1 = x - 5, y - 10
    x1, y1 = (x + cos_angle * -5 - sin_angle * -10, y + sin_angle * -5 + cos_angle * -10)
    x2, y2 = x, y
    x3, y3 = x + 5, y - 10
    x3, y3 = (x + cos_angle * 5 - sin_angle * -10, y + sin_angle * 5 + cos_angle * -10)

    if fill:
        return f'<polygon points="{x1} {y1} {x2} {y2} {x3} {y3}" fill="{color}"/>'
    else:
        return f'<polygon points="{x1} {y1} {x2} {y2} {x3} {y3}" stroke="{color}" fill="none"/>'

def textwrap(x, source: str, line_width = 16) -> str:
    lines: list[list[str]] = [[]]
    for word in source.split():
        if sum(map(len, lines[-1])) + len(word) < line_width:
            lines[-1].append(word)
        else:
            lines.append([word])

    spans = []
    for i, line in enumerate(lines):
        dy = 'dy="14"' if i > 0 else ''
        spans.append(f'<tspan x="{int(x)}" {dy}>{escape(" ".join(line))}</tspan>')
    return ''.join(spans)