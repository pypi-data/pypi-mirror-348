from typing import Optional, Any
from jupyter_server.services.sessions.sessionmanager import SessionManager

class MySessionManager(SessionManager):
    
    async def create_session(
        self,
        path: Optional[str] = None,
        name = None,
        type: Optional[str] = None,
        kernel_name = None,
        kernel_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        After creating a session, connects the yroom to the kernel client.
        """
        print("INCOMING PATH")
        print(path)
        output = await super().create_session(
            path,
            name,
            type,
            kernel_name,
            kernel_id
        )
        return output

c.ServerApp.session_manager_class = MySessionManager