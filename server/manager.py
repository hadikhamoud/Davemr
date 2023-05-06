import os
import json
from top_3_algorithms import get_text_score
from book import Book

class GraphManager:
    
        ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
        
        
        def __init__(self, chosen_book_number = 3):
            
            self.algorithm_scoring, self.algorithm_node_scoring = dict(), dict()
            self.input_so_far = ['']
            self.top_nodes = [] 
            self.cyto_graphs = json.load(open(os.path.join(GraphManager.ROOT_DIR, "data/cyto_graphs.json")))
            self.books = self.get_books()
            self.set_book(chosen_book_number)
                
        def set_book(self, choice):
            self.chosen_book = self.get_book_by_number(choice)
            self.clear_all()
            self.algorithm_scoring, self.algorithm_node_scoring = self.populate_algorithm_scoring_maps(chosen_book = self.chosen_book)
            
        
        def get_book_by_number(self, number):
            for book in self.books:
                if book.get_book_number() == number:
                    return book
 
        #clear all elements in dictionary
        def clear_all(self):
            self.algorithm_scoring = dict.fromkeys(self.algorithm_scoring, 0)
            self.algorithm_node_scoring = dict.fromkeys(self.algorithm_node_scoring, [])
            self.input_so_far = ['']
            self.TopNodes = []
            
            
            
        def get_books(self):
            books = []
            for book in os.listdir(os.path.join(GraphManager.ROOT_DIR, "books")):
                #get the book name
                book_number = int(book.split("_")[0])
                
                #create book object and return it
                books.append(Book(book, book_number))
                
                #sort books by book number
            return sorted(books, key=lambda book: book.book_number)
        
        
        def get_cyto_graph(self, graph_name): 
                if graph_name in self.cyto_graphs:
                    return self.cyto_graphs[graph_name]
                else:
                    print(f'{graph_name} does not exist')
                    return None
                

        def populate_algorithm_scoring_maps(self, chosen_book):
            algorithm_scoring = {}
            algorithm_node_scoring = {}
                        
            for file in os.listdir(chosen_book.graph_dir):
                try:
                    algorithm_scoring[file] = 0
                except:
                    continue
            for file in os.listdir(chosen_book.graph_dir):
                try:
                    algorithm_node_scoring[file] = []
                except:
                    continue
                
            return algorithm_scoring, algorithm_node_scoring
        
        
        def _get_top_algorithms_and_scores(self, start_rank, num_graphs):
            sorted_algorithms = dict(sorted(self.algorithm_scoring.items(), key=lambda item: item[1], reverse=True))
            top_algorithms = list(sorted_algorithms.keys())[start_rank - 1: start_rank - 1 + num_graphs]
            top_scores = list(sorted_algorithms.values())[start_rank - 1: start_rank - 1 + num_graphs]
            return top_algorithms, top_scores

        def _get_graph_elements_and_names(self, top_algorithms):
            graph_elements = [self.get_cyto_graph(key) for key in top_algorithms]
            graph_names = [self.chosen_book.graph_name_repr[key] for key in top_algorithms]
            return graph_elements, graph_names

        def get_graphs_and_scores(self, text = None, start_rank = 1, num_graphs = 3):
            if text:
                self.input_so_far = get_text_score(self.algorithm_scoring, self.chosen_book.hashmap, text, self.algorithm_node_scoring, self.input_so_far)

            top_algorithms, top_scores = self._get_top_algorithms_and_scores(start_rank, num_graphs)
            graph_elements, graph_names = self._get_graph_elements_and_names(top_algorithms)

            response_data = {
                "Stall": len(self.input_so_far) < 5,
                "elements": graph_elements,
            }

            for ind, (name, elements, score) in enumerate(zip(graph_names, graph_elements, top_scores)):
                index = start_rank+ind
                response_data[f"NameG{index}"] = name
                response_data[f"elementsG{index}"] = elements
                response_data[f"ScoreG{index}"] = round(score, 2)
            
            self.print_graphs_and_scores(top_algorithms, graph_names, top_scores) 
            
                

            return response_data
        
        def print_graphs_and_scores(self, top_algorithms, graph_names, top_scores):
            print(f"Input: {self.input_so_far}")
            for algorithm, name, score in zip(top_algorithms, graph_names, top_scores):
                print(f"Graph: {name} (Algorithm: {algorithm}) - Score: {round(score, 2)}")

                
      