from bisslog.use_cases.use_case_full import FullUseCase


class MySecondUseCase(FullUseCase):

    def use(self, value: float, product_type: str, *args, **kwargs) -> float:

        self.log.info("Se recibió valor %d %s", value, self._transaction_manager.get_component(), checkpoint_id="second-reception")

        if product_type == "string1":
            new_value = value * .2
        elif product_type == "string2":
            new_value = value * .3
        elif product_type == "string3":
            new_value = value * .5
        else:
            new_value = value * .05

        uploaded = self.upload_file_from_local("./test.txt", "/app/casa/20")

        if uploaded:

            self.log.info("Uploaded file component: %s", self._transaction_manager.get_component(), checkpoint_id="uploaded-file")

        return new_value


my_second_use_case = MySecondUseCase()
