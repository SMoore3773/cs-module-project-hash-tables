class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        if isinstance(other, HashTableEntry):
            return self.key == other.key
        return False

    def __repr__(self):
        return f'HashTableEntry({self.key}, {self.value})'

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return f'Node({self.value})'

class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        curStr = ""
        cur = self.head
        while cur is not None:
            curStr += f'{str(cur.value)} -> '
            cur = cur.next
        return curStr

    def find(self, value):
        cur = self.head

        while cur is not None:
            if cur.value == value:
                return cur

            cur = cur.next

        return None

    def delete(self, value):
        cur = self.head

        # Special case of deleting head

        if cur.value == value:
            self.head = cur.next
            return cur

        # General case of deleting internal node

        prev = cur
        cur = cur.next

        while cur is not None:
            if cur.value == value:  # Found it!
                prev.next = cur.next   # Cut it out
                cur.next = None
                return cur  # Return deleted node
            else:
                prev = cur
                cur = cur.next

        return None  # If we got here, nothing found

    def insert_at_head(self, node):
        node.next = self.head
        self.head = node

    def insert_at_head_or_overwrite(self, node):
        existingNode = self.find(node.value)
        if existingNode is not None:
            existingNode.value = node.value
            return False
        else:
            self.insert_at_head(node)
            return True

class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # Your code here
        # intitailize table
        self.table = [None] * capacity
        self.capacity = capacity
        self.entries = 0
        # instance of linked list to access ll methods for collision resolution


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # return the total length of the table
        return len(self.table)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # LF = number of items in hash table devided by the number of spaces in the table
        return self.entries / self.get_num_slots()

    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here

    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for x in key:
            hash = ((hash << 5) + hash) + ord(x)
        return hash & 0xFFFFFFFF

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # returns the hash of the key of the object to be stored

        return self.djb2(key) % self.get_num_slots()

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # for a table with no collisions
        # self.table[self.hash_index(key)] = value

        # points to the location of the table assigned to the hashed key, then creates an instance of a linked list at that location
        # self.table[self.hash_index(key)] = ll.insert_at_head_or_overwrite(HashTableEntry(key, value))

        # # increment the number of entries to keep track of load factor
        # self.entries += 1
        # if self.get_load_factor() > 0.7:
        #     self.resize(self.capacity * 2)
        hash_index = self.hash_index(key)
        if self.table[hash_index] != None:
            linked_list = self.table[hash_index]
            did_add_new_node = linked_list.insert_at_head_or_overwrite(Node(HashTableEntry(key, value)))
            if did_add_new_node:
                self.entries += 1
        else:
            linked_list = LinkedList()
            linked_list.insert_at_head(Node(HashTableEntry(key, value)))
            self.table[hash_index] = linked_list
            self.entries += 1

        if self.get_load_factor() > 0.7:
            self.resize(self.get_num_slots() * 2)

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        # value = self.table[self.hash_index(key)]

        # if value == None:
        #     print('value is None')
        # for a list with no collisions
        # self.table[self.hash_index(key)] = None

        # for a list that has linked list collision resolution
        # self.table[self.hash_index(key)] = ll.delete(key)

        # self.entries -= 1
        # # run resize if load factor is too small after deletion
        # if self.get_load_factor() < 0.3:
        #     self.resize(self.capacity / 2)

        hash_index = self.hash_index(key)
        if self.table[hash_index] != None:
            linked_list = self.table[hash_index]
            did_delete_node = linked_list.delete(HashTableEntry(key, None))
            if did_delete_node != None:
                self.entries -= 1
                if self.get_load_factor() < 0.2:
                    self.resize(self.get_num_slots() / 2)
        else:
            print("Warning: node not found")

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # for a table with no collisions
        # return self.table[self.hash_index(key)]
        # get to the index of the table, then traverse the linked list there to get the value
        hash_index = self.hash_index(key)
        if self.table[hash_index] != None:
            linked_list = self.table[hash_index]
            node = linked_list.find(HashTableEntry(key, None))
            if node != None:
                return node.value.value
        return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # check load factor to determine if new capacity is going to be larger or smaller
        old_table = self.table
        self.table = [None] * int(new_capacity)
        self.entries = 0

        for element in old_table:
            if element == None:
                continue
            curr_node = element.head
            while curr_node != None:
                temp = curr_node.next
                curr_node.next = None
                hash_index = self.hash_index(curr_node.value.key)

                if self.table[hash_index] != None:
                    linked_list = self.table[hash_index]
                    linked_list.insert_at_head(curr_node)
                else:
                    linked_list = LinkedList()
                    linked_list.insert_at_head(curr_node)
                    self.table[hash_index] = linked_list

                curr_node = temp
                self.entries += 1

        # if new_capacity > self.capacity:
        #     pass
        #     # new capacity will be double current capacity
        # if new_capacity < self.capacity:
        #     pass
        #     # new capacity will be half current capacity
        # else:
        #     pass


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
