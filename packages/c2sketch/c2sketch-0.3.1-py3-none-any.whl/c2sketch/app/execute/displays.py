"""Support for displaying specific information spaces on dedicated displays"""
from toppyt import view_information

__all__ = ['view_public_display']

def view_public_display(model_store, execution_store, plugin_loader, display_name):
    return view_information('test')



# def view_public_display(planstore, executestore, plugins: PluginLoader, screen_name):

#     def view_display(screen_name):
#         return with_information(executestore, lambda es:es.last_active_op(screen_name),view_info_space)
   
#     def view_info_space(ifs_def):
#         if ifs_def is None:
#             return view_information('Not configured')
        
#         plan_id, ifs_instance_id, ifs_id = ifs_def
        
#         def view(plan: Model):
#             ifs = plan.get_info_space_by_id(ifs_id)
#             if ifs.visualization_plugin in plugins.visualizations:
#                 viz = plugins.visualizations[ifs.visualization_plugin]

#                 ifs_type = None if ifs.type is None else plan.get_record_type(ifs.type)
#                 ifs_read_source = (executestore,lambda es: es.info_space_complete(plan_id, ifs_instance_id))
#                 return viz.control_ui(ifs_read_source,None,ifs_type,ifs.visualization_config)
#             else:
#                 return constant(None)
    
#         return with_information(planstore,lambda ps: ps.plan(plan_id),view,refresh=False)
    
#     def display_layout(parts):
#         return f'''
#         <div style="min-height: 100vh; background: black; color: white">
#         {parts['task']}
#         </div>
#         '''
        
#     return ParallelTask([('task',view_display(screen_name))],layout=display_layout)