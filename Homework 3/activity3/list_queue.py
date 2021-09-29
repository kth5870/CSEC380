
class Queue:
    def __init__(self):
        self.links = []
        self.size = 0

    def is_empty(self):
        return self.size <= 0

    def peek(self):
        return self.links[0]

    def enqueue(self, url, depth):
        if url == "":
            url = "/"
        data = (url, depth)
        if data not in self.links:
            self.links.append(data)
            self.size += 1
        else:
            pass

    def dequeue(self):
        if self.is_empty():
            print("Empty Queue - Cannot dequeue")
        else:
            first = self.links[0]
            self.links.remove(first)
            self.size -= 1
            return first

    def size(self):
        return self.size

    def get_values(self):
        for item in self.links:
            print(item)




