import gazu
from langchain_core.tools import tool

HOST = os.getenv("KITSU_HOST", "http://localhost:5000/api")
configure_kitsu_ca_bundle(HOST)
gazu.client.set_host(HOST)
gazu.log_in("api_user", "123456")

@tool
def get_shot_comp_status(project_name: str, sequence_name: str, shot_name: str) -> str:
    """
    Fetches the current status of the 'Compositing' task for a specific shot in Kitsu.
    Use this when the user asks about the status of a shot.
    """
    try:
        project = gazu.project.get_project_by_name(project_name)
        if not project: return f"Project '{project_name}' not found."
        
        shot = gazu.shot.get_shot_by_name(project, shot_name, sequence_name)
        if not shot: return f"Shot '{shot_name}' not found in sequence '{sequence_name}'."

        task_type = gazu.task.get_task_type_by_name("Compositing")
        task = gazu.task.get_task_by_entity(shot, task_type)
        
        if not task: return "Compositing task not found for this shot."
        return f"The current status of Compositing for shot {shot_name} is: {task['task_status_name']}"

    except Exception as e:
        return f"Error communicating with Kitsu API: {str(e)}"