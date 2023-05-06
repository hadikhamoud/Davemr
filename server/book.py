import os
import json

class Book:
    
    
    """
    within the project, books and their data fall in this structure tree
    books
        - self.name
            - graphs
            - hashmap.json
            - graph_name_repr.json
    """
    
    ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
    
    
    def __init__(self, name, book_number = 1):
        
        
        self.name = name
        self.book_number = book_number
        
        graph_dir_path = f"books/{name}/graphs"
        self.graph_dir = self.get_file(graph_dir_path, file=False)
        
        hashmap_path = f"books/{name}/hashmap.json"
        self.hashmap = self.get_file(hashmap_path, file=True)
        
        graph_name_repr_path = f"books/{name}/graph_name_repr.json"
        self.graph_name_repr =  self.get_file(graph_name_repr_path, file=True)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def get_book_number(self):
        return self.book_number
    
    def get_file(self, path, file= False):
        file_path = os.path.join(Book.ROOT_DIR, path)
        if file: 
            return json.load(open(file_path))
        return file_path
    
    def get_graph_name(self, graph_name):
        return self.graph_name_repr[graph_name]
        
    