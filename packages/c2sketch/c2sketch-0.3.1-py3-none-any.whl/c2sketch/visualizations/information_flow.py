from ..models import *
import networkx as nx

__all__ = [
    'nx_actor_information_flow',
    'dot_actor_information_flow'
]

def nx_actor_information_flow(models: ModelSet, model_id: ModelID) -> nx.MultiDiGraph:
    """
    Create a graph that connects actors and information spaces.
    Simple (non-compound) tasks are used as edges.
    For all actors that can perform the task an edge is created between
    the actor and the information spaces that are used by the task.
    
    """
    model = models.get_model_by_id(model_id)

    graph = nx.MultiDiGraph()
    tasks = collect_atomic_task_nodes(model)

    individuals = list_individuals(models,model_id)
   
    graph_actors = set()
    graph_info_spaces = set()
    graph_tasks = set()

    for task in tasks:
        
        #Who can work on the task
        actor_constraints = resolve_task_actor_constraints(task)
        
        task_actors = set()
        for actor_id in individuals:
            actor_orgs = list_actor_affiliations(models, model_id, actor_id)
            allowed = True
            for required in actor_constraints:
                if not required in actor_orgs:
                    allowed = False
                    break
            if allowed:
                task_actors.add(actor_id)
       
        #Which information spaces are used
        info_spaces = resolve_info_space_bindings(models,task)

        for (req, binding) in info_spaces.values():
            if binding is None: #Unknown which info space is used
                continue

            ifs_id = binding.node_id
            if ifs_id not in graph_info_spaces:
                graph.add_node(f'ifs_{ifs_id}', type='info_space', name=binding.name)
                graph_info_spaces.add(ifs_id)

            for actor_id in task_actors:
                if actor_id not in graph_actors:
                    actor = models.get_actor_by_id(actor_id)
                    graph.add_node(f'actor_{actor_id}', type='actor', name = actor.name)
                    graph_actors.add(actor_id)
              
                if req.read: #Information flows in
                    link_id = (f'ifs_{ifs_id}', f'actor_{actor_id}',task.name)
                    if link_id not in graph_tasks:
                        graph.add_edge(f'ifs_{ifs_id}', f'actor_{actor_id}', task=task.name)
                        graph_tasks.add(link_id)
                if req.write: #Information flows out
                    link_id = (f'actor_{actor_id}', f'ifs_{ifs_id}',task.name)
                    if link_id not in graph_tasks:
                        graph.add_edge(f'actor_{actor_id}', f'ifs_{ifs_id}', task=task.name)
                        graph_tasks.add(link_id)
     
    return graph
  
def dot_actor_information_flow(models: ModelSet, model_id: ModelID) -> str:

    graph = nx_actor_information_flow(models, model_id)
    for node in graph.nodes.values():
        node['label'] = node['name']
        if node['type'] == 'info_space':
            node['shape'] = 'oval'
        if node['type'] == 'actor':
            node['shape'] = 'rect'
            node['style'] = 'rounded'
    for u, v, w, task in graph.edges(data='task',keys=True): #type: ignore
        graph.edges[u,v,w]['label'] = task

    return nx.nx_agraph.to_agraph(graph).to_string()