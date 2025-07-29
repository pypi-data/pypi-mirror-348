from ..models import Model, ModelSet, ModelID, Import, Attribute, Constraint, Actor, ActorMember, ActorGroup, InformationSpace, Task, TaskDefinition, TaskInstance
from ..models import resolve_indirect_imports, collect_atomic_task_nodes, resolve_info_space_bindings
import networkx as nx

__all__ = ('nx_full_network',
           'nx_full_model',
           'nx_actor_network',
           'nx_location_network',
           'nx_information_flow',
           )

def nx_full_model(model: Model) -> nx.MultiDiGraph:
    """Raw dump of information of a C2Sketch model to a networkx graph"""
    
    graph = nx.MultiDiGraph()
    model_id = f'model-{model.id}'
    graph.add_node(model_id, node_type = 'model')

    def add_node(graph: nx.MultiDiGraph, node, parent_id, parent_node):
        match node:
            case Import(reference):
                import_id = f'import-{parent_node.node_id}-{reference}'
                graph.add_node(import_id,node_type='import',reference=reference)
                graph.add_edge(import_id,parent_id)
            case Attribute(name,value):
                attribute_id = f'attribute-{parent_node.node_id}-{name}'
                graph.add_node(attribute_id,node_type='attribute',name=name,value=value)
                graph.add_edge(attribute_id,parent_id)
            case Constraint(name,value):
                attribute_id = f'constraint-{parent_node.node_id}-{name}'
                graph.add_node(attribute_id,node_type='constraint',name=name,value=value)
                graph.add_edge(attribute_id,parent_id)
            case Actor():
                actor_id = f'actor-{node.node_id}'
                graph.add_node(actor_id,node_type='actor')
                graph.add_edge(actor_id,parent_id)
                for sub_node in node.nodes:
                    add_node(graph, sub_node, actor_id, node)
            case ActorMember(actor_id):
                member_id = f'actor-member-{parent_node.node_id}-{actor_id}'
                graph.add_node(member_id, node_type='member', actor_id=actor_id)
                graph.add_edge(member_id,parent_id)
            case ActorGroup(actor_id):
                group_id = f'actor-group-{parent_node.node_id}-{actor_id}'
                graph.add_node(group_id, node_type='group', actor_id=actor_id)
                graph.add_edge(group_id,parent_id)
            case InformationSpace(name):
                ifs_id = f'infospace-{node.node_id}'
                graph.add_node(ifs_id,node_type='information-space')
                graph.add_edge(ifs_id,parent_id)
                for sub_node in node.nodes:
                    add_node(graph, sub_node, ifs_id, node)
            case Task(name):
                task_id = f'task-{node.node_id}'
                graph.add_node(task_id,node_type='task')
                graph.add_edge(task_id,parent_id)
                for sub_node in node.nodes:
                    add_node(graph, sub_node, task_id, node)
            case TaskDefinition(name):
                taskdef_id = f'taskdef-{node.node_id}'
                graph.add_node(taskdef_id,node_type='task-definition')
                graph.add_edge(taskdef_id,parent_id)
                for sub_node in node.nodes:
                    add_node(graph, sub_node, taskdef_id, node)
            case TaskInstance(name):
                task_id = f'taskinstance-{node.node_id}'
                graph.add_node(task_id,node_type='task-instance')
                graph.add_edge(task_id,parent_id)
                for sub_node in node.nodes:
                    add_node(graph, sub_node, task_id, node)

    for node in model.nodes:
        add_node(graph,node,model_id, model)

    return graph

def nx_actor_network(models: ModelSet, model_id: ModelID) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
 
    for imported_id in resolve_indirect_imports(models,model_id):
        model = models.get_model_by_id(imported_id)
     
        # Add actors
        for actor in model.actors:
            attributes = {attr.name : attr.value for attr in actor.nodes if isinstance(attr,Attribute)}
            graph.add_node(f'actor_{actor.name}',node_type='actor',**attributes)

        # Add relations
        for actor in model.actors:
            for member in actor.members:
                member_actor = model.get_actor_by_id(member)
                graph.add_edge(f'actor_{member_actor.name}',f'actor_{actor.name}')
            for group in actor.groups:
                group_actor = model.get_actor_by_id(group)
                graph.add_edge(f'actor_{actor.name}',f'actor_{group_actor.name}')
        
    return graph

def nx_location_network(models: ModelSet, model_id: ModelID) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
 
    for imported_id in resolve_indirect_imports(models,model_id):
        model = models.get_model_by_id(imported_id)
     
        # Add locations
        for location in model.locations:
            attributes = {attr.name : attr.value for attr in location.nodes if isinstance(attr,Attribute)}
            graph.add_node(f'location_{location.name}',node_type='location',**attributes)

        # Add relations
        for location in model.locations:
            for member in location.members:
                member_location = model.get_location_by_id(member)
                graph.add_edge(f'location_{member_location.name}',f'location_{location.name}')
            for group in location.groups:
                group_location = model.get_location_by_id(group)
                graph.add_edge(f'location_{location.name}',f'location_{group_location.name}')
        
    return graph



def nx_full_network(plan: Model) -> nx.MultiDiGraph:
    #DEPRECATED
    graph = nx.MultiDiGraph()
    for actor in plan.actors:
        attributes = {'type':'actor','name':actor.name}
        if actor.annotations is not None:
            for name, value in actor.annotations.items():
                attributes[f'annotation_{name}'] = value
        graph.add_node(f'actor_{actor.name}', **attributes)
    for actor in plan.actors:
        for affiliation in actor.groups:
            graph.add_edge(f'actor_{actor.name}',f'actor_{affiliation}',relation='affiliation')

    def add_task_nodes(graph: nx.MultiDiGraph, parent: str, tasks: list[Task]) -> None:
        for task in tasks:
            attributes = {'type':'task','name': task.name}
            if task.annotations is not None:
                for name, value in task.annotations.items():
                    attributes[f'annotation_{name}'] = value
            graph.add_node(f'task_{task.node_id}',**attributes)
            graph.add_edge(f'task_{task.node_id}',parent,relation='part_of')
    
            # Add locally defined information spaces
            for ifs in task.info_spaces:
                attributes = {'type':'info_space','name': ifs.name}
                if ifs.annotations is not None:
                    for name, value in ifs.annotations.items():
                        attributes[f'annotation_{name}'] = value

                graph.add_node(f'ifs_{ifs.node_id}',**attributes)
                graph.add_edge(f'task_{task.node_id}',f'ifs_{ifs.node_id}',relation='part_of')

            # Add used information spaces
            info_space_bindings = task.resolve_info_space_bindings()
            for ifs in info_space_bindings.values():
                if ifs is None:
                    continue
                graph.add_edge(f'task_{task.node_id}',f'ifs_{ifs_id}',relation='requires')
            # Add triggering information spaces
            if task.triggers:
                for trigger in task.triggers:
                    ifs_id = task.resolve_info_space(trigger)
                    if ifs_id is not None:
                        graph.add_edge(f'ifs_{ifs_id}', f'task_{task.node_id}', relation='triggers')  
            
            add_task_nodes(graph,f'task_{task.node_id}',task.tasks)

    add_task_nodes(graph,'root',plan.tasks)

    return graph


def nx_information_flow(models: ModelSet, model_id) -> nx.MultiDiGraph:
    """Create a graph that shows how information is transferred between information spaces through tasks"""
    
    # Main idea:
    # - The nodes in the graph are all information spaces
    # - The edges in the graph are all non-compound tasks that use information spaces
    # - Edges are created for all pairs of information spaces used in the task:
    #   - That the task reads as origin of an edge
    #   - That the task writes as destination of an edge
    
    graph = nx.MultiDiGraph()

    model = models.get_model_by_id(model_id)

    #All information spaces are nodes in the graph
    for ifs in model.info_spaces:
        attributes = {attr.name : attr.value for attr in ifs.nodes if isinstance(attr,Attribute)}
        attributes['label'] = ifs.label
        ifs_id = f'infospace-{ifs.node_id}'
        graph.add_node(ifs_id,node_type='information-space',**attributes)
    
    #Collect all atomic (non-compound) tasks in the task tree
    task_nodes = collect_atomic_task_nodes(model)
    for node in task_nodes:
        #Determine which information spaces are used
        bound_info_spaces = resolve_info_space_bindings(node)
        if bound_info_spaces:
            #Connect all spaces from which information is read to spaces to which information is written
            read_spaces = [ifs for (req, ifs) in [v for v in bound_info_spaces.values() if v is not None] if req.read]
            write_spaces = [ifs for (req, ifs) in [v for v in bound_info_spaces.values() if v is not None] if req.write]

            for read_ifs in read_spaces:
                for write_ifs in write_spaces:
                    attributes = {attr.name : attr.value for attr in node.nodes if isinstance(attr,Attribute)}
                    attributes['label'] = node.label
                    graph.add_edge(f'infospace-{read_ifs.node_id}',f'infospace-{write_ifs.node_id}',task=node.node_id,**attributes)
 
    return graph