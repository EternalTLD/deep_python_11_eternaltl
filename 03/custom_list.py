class CustomList(list):
    @staticmethod
    def _prepare_lists(list1, list2):
        list1 = CustomList(list1)
        list2 = CustomList(list2)
        if len(list1) > len(list2):
            list2.extend([0 for _ in range(len(list1) - len(list2))])
        else:
            list1.extend([0 for _ in range(len(list2) - len(list1))])
        return list1, list2

    def __add__(self, other):
        if not isinstance(other, list):
            raise TypeError("Addition operation can only be performed on lists")

        list1, list2 = self._prepare_lists(self, other)
        result_list = []
        for _, (element1, element2) in enumerate(zip(list1, list2)):
            result_list.append(element1 + element2)
        return CustomList(result_list)

    def __radd__(self, other):
        if not isinstance(other, list):
            raise TypeError("Addition operation can only be performed on lists")

        list1, list2 = self._prepare_lists(self, other)
        result_list = []
        for _, (element1, element2) in enumerate(zip(list1, list2)):
            result_list.append(element1 + element2)
        return CustomList(result_list)

    def __sub__(self, other):
        if not isinstance(other, list):
            raise TypeError("Subtraction operation can only be performed on lists")

        list1, list2 = self._prepare_lists(self, other)
        result_list = []
        for _, (element1, element2) in enumerate(zip(list1, list2)):
            result_list.append(element1 - element2)
        return CustomList(result_list)

    def __rsub__(self, other):
        if not isinstance(other, list):
            raise TypeError("Subtraction operation can only be performed on lists")

        list1, list2 = self._prepare_lists(self, other)
        result_list = []
        for _, (element1, element2) in enumerate(zip(list1, list2)):
            result_list.append(element2 - element1)
        return CustomList(result_list)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __str__(self) -> str:
        return f"CustomList({list(self)}), sum - {sum(self)}"
