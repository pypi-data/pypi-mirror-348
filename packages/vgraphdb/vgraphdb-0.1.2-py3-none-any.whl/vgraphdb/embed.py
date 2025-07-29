import pickle
import torch
from sklearn.model_selection import train_test_split
from TorusE import TorusE

class Pipeline:
    def __init__(self, triples_filename):
        """Initialize the Pipeline with a triples filename."""
        self.triples_filename = triples_filename
        self.train_triples = None
        self.test_triples = None
        self.num_entities = None
        self.num_relations = None
        self.entity_dict = None
        self.predicate_dict = None

    def extract_entities_predicates(self, triples, sorted=False):
        """
        Extract unique entities and predicates from a list of triples and assign indexes.
        
        Args:
            triples: List of tuples, each containing (subject, predicate, object).
            sorted: If True, sort entities and predicates for consistent indexing.
        
        Returns:
            tuple: (entity_dict, predicate_dict)
                - entity_dict: Dict mapping unique entities to integer indexes.
                - predicate_dict: Dict mapping unique predicates to integer indexes.
        """
        entities = set()
        predicates = set()
        
        for subject, predicate, object_ in triples:
            entities.add(subject)
            entities.add(object_)
            predicates.add(predicate)
        
        if sorted:
            entities = sorted(entities)
            predicates = sorted(predicates)
        
        entity_dict = {entity: idx for idx, entity in enumerate(entities)}
        predicate_dict = {predicate: idx for idx, predicate in enumerate(predicates)}
        
        return entity_dict, predicate_dict

    def handle_dataset(self, train_ratio=0.9, random_seed=42):
        """
        Process the dataset from the triples file and store train_triples, num_entities, num_relations.
        
        Args:
            triples_filename: Path to the triples file (default: None, uses self.triples_filename).
            train_ratio: Fraction of triples to use for training (default: 0.9).
            random_seed: Seed for reproducible train-test split (default: 42).
        """
        # Use provided triples_filename or fall back to self.triples_filename
        filename = self.triples_filename
        
        # Load triples from file
        with open(filename, 'rb') as f:
            triples_all = pickle.load(f)
            print(f"Loaded triples from {filename}")

        # Extract entities and predicates
        self.entity_dict, self.predicate_dict = self.extract_entities_predicates(triples_all)
        
        # Store num_entities and num_relations
        self.num_entities = len(self.entity_dict)
        self.num_relations = len(self.predicate_dict)
        print(f"Entity Dictionary: ({self.num_entities})")
        print(f"Predicate Dictionary: ({self.num_relations})")
        
        # Index the triples
        indexed_triples = [
            (self.entity_dict[s], self.predicate_dict[p], self.entity_dict[o])
            for s, p, o in triples_all
        ]
        
        # Split into train and test triples
        self.train_triples, self.test_triples = train_test_split(
            indexed_triples, train_size=train_ratio, random_state=random_seed
        )
        print(f"Created {len(self.train_triples)} training triples and {len(self.test_triples)} test triples")

        # Save entity dictionary (optional, kept for compatibility)
        entity_dict_fn = './store/entity_dict.pk'
        with open(entity_dict_fn, 'wb') as f:
            pickle.dump(self.entity_dict, f)
            print(f"Writing entity dictionary to {entity_dict_fn}")

    def handle_training(self, num_epochs=10, emb_dim=30, lr=1e-3, device='mps'):
        """
        Train the TorusE model using stored train_triples, num_entities, and num_relations.
        
        Args:
            num_epochs: Number of training epochs (default: 10).
            emb_dim: Embedding dimension (default: 30).
            lr: Learning rate (default: 1e-3).
            device: Device to run the model on (default: 'mps').
        """
        if self.train_triples is None or self.num_entities is None or self.num_relations is None:
            raise ValueError("Dataset must be processed first. Run handle_dataset().")

        device = torch.device(device)
        model = TorusE(
            self.num_entities,
            self.num_relations,
            device,
            emb_dim=emb_dim,
            lr=lr
        ).to(device)
        
        print(f"Training model with {self.num_entities} entities and {self.num_relations} relations")
        model._train(self.train_triples, num_epochs=num_epochs)
        
        # Save entity embeddings
        embds_fn = './store/entity_embds.pt'
        torch.save(model.entity_embds.detach().cpu(), embds_fn)
        print(f"Saved entity embeddings to {embds_fn}")

    def run(self):
        """
        Run the full pipeline: process dataset and train the model.
        
        Args:
            triples_filename: Path to the triples file (default: '../../data/triples_demo.pk').
        """
        print("Starting pipeline execution...")
        self.handle_dataset()
        self.handle_training()
        print("Pipeline execution completed.")