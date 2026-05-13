import logging
import os
from datetime import datetime
from app.core.config import settings

class AuditLogger:
    def __init__(self):
        self.log_file = os.path.join(settings.UPLOAD_DIR, "audit_log.txt")
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("ContaDocAudit")

    def log_action(self, user: str, action: str, client_id: str, details: str):
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"USER: {user} | ACTION: {action} | CLIENT: {client_id} | DETAILS: {details}"
        self.logger.info(log_entry)

audit_logger = AuditLogger()
