from random import random

from bisslog.database.bisslog_db import bisslog_db as db
from bisslog.use_cases.use_case_full import FullUseCase
from scripts.project_example_1.usecases.my_second_use_case import my_second_use_case



class SumarUseCase(FullUseCase):

    def use(self, a: int, b: int, user_id: int, transaction_id: str, *args, **kwargs) -> dict:
        component = self._transaction_manager.get_component()
        self.log.info("Se recibe a:%d b:%d %s", a, b, component, checkpoint_id="reception",
                      transaction_id=transaction_id)
        last_session = db.session.get_last_session_user(user_id)
        if last_session is not None:
            self.log.info(f"La última sesión del usuario {user_id} fue {last_session}", checkpoint_id="last_session")
        db.session.save_new_session_user(user_id)

        db.event_type.loadWebhookEventType(5)
        rand = random()
        new_value = my_second_use_case(
            value=rand*10, product_type="string2", transaction_id=transaction_id)

        res = a + b
        if res > 10:
            self.log.warning("Es mayor que 10", checkpoint_id="check-response")

        self.publish("queue_suma", {"suma": res + new_value, "operation" : "a + b"})
        return {"suma": res}


sumar_use_case = SumarUseCase("sumar")
