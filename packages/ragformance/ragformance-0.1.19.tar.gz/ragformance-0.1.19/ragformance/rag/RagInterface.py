from abc import abstractmethod  

class RagInterface:
    
    @abstractmethod
    def upload_corpus(corpus,configpath="config.json"):
        raise NotImplementedError

    @abstractmethod
    def ask_queries(queries, configpath="config.json"):
        raise NotImplementedError



        