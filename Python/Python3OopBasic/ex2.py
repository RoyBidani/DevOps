class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def push(self,value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def pop(self):
        if self.head is None:
            return None
        elif self.head.next is None:
            value = self.head.value
            self.head = None
            return value
        else:
            current = self.head
            while current.next.next:
                current = current.next
            value = current.next.value
            current.next = None
            return value

    def get_head(self):
        if self.head:
            return self.head.value
        else:
            return None

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def is_empty(self):
        return self.head is None


my_list = LinkedList()

my_list.push(1)
my_list.push(2)
my_list.push(3)

print(len(my_list))
print(my_list.get_head())

removed = my_list.pop()
print(removed)

print(len(my_list))
print(my_list.is_empty())

