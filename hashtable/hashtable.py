class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        currStr = ''
        curr = self.head
        while curr != None:
            currStr += f'{str(curr.value)} ->'
            curr = curr.next
        return currStr

    def find(self, value):
        # return node with value
        curr = self.head

        while curr != None:
            if curr.value == value:
                return curr
            curr = curr.next
        return None

    # delete node with given value
    # O(n)
    def delete(self, value):
        curr = self.head
        prev = None
        # if value to delete is head
        if curr.key == value:
            self.head = curr.next
            curr.next = None
            return curr

        while curr != None:
            if curr.key == value:
                prev.next = curr.next
                curr.next = None
                return curr
            else:
                prev = curr
                curr = curr.next

        return None

    def insert_at_head(self, node):
        node.next = self.head
        self.head = node

    # overwright node or insert node at the head
    def insert_at_head_or_overwrite(self, node):
        existingNode = self.find(node.value)
        if existingNode != None:
            existingNode.value = node.value
        else:
            self.insert_at_head(node)


# counter to determine load factor, will be incremented for puts, and decremented for deletes

# instance of linked list to access ll methods for collision resolution
ll = LinkedList()


class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


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
        return (self.entries / self.capacity)

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

        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        self.table[self.hash_index(key)] = value
        # points to the location of the table assigned to the hashed key, then creates an instance of a linked list at that location
        # self.table[self.hash_index(key)] = ll.insert_at_head_or_overwrite(HashTableEntry(key, value))

        # increment the number of entries to keep track of load factor
        # entries += 1

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        value = self.table[self.hash_index(key)]

        if value == None:
            print('value is None')
        self.table[self.hash_index(key)] = None
        # self.table[self.hash_index(key)] = ll.delete(key)

        # entries -= 1
        # run resize if load factor is too small after deletion
        # self.resize()

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        value = self.table
        return self.table[self.hash_index(key)]

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # check load factor to determine if new capacity is going to be larger or smaller
        lf = self.get_load_factor()
        if lf > 0.7:
            pass
            # new capacity will be double current capacity
        if lf < 0.3:
            pass
            # new capacity will be half current capacity
        else:
            pass


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
