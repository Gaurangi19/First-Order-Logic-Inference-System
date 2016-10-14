# First-Order-Logic-Inference-System

Given a knowledge base and a query sentence, the program determines if the query can be inferred from the knowledge base using Backward Chaining algorithm for first-order logic.

**Input**  
You will be given a knowledge base and the query in a text file ending with a .txt extension.  
The first line of the input file contains the query. The query can have three forms:  
1) as a fact with a single atomic sentence:  
e.g. Traitor(Anakin)  
2) as several facts with multiple atomic sentences, separated by ‘ && ’:  
e.g. Knows(Sidious, Pine) && Traitor(Anakin)  
3) as a single predicate with one unknown variable:  
e.g. Traitor(x)  
The second line contains an integer n specifying the number of clauses in the knowledge base.  
The remaining lines contain the clauses in the knowledge base, one per line . Each clause is written in one of the following forms:
1) as an implication of the form p1 ∧ p2 ∧ ... ∧ pn ⇒ q , whose premise is a conjunction of atomic sentences and whose conclusion is a single atomic sentence.  
2) as a fact with a single atomic sentence: q . Each atomic sentence is a predicate applied to a certain number of arguments.

**Output**  
The process of backwardchaining should be printed to a file called output.txt . Given the sample input above, the output content should be as follows:  
Ask: Traitor(Anakin)  
Ask: ViterbiSquirrel(Anakin)  
True: ViterbiSquirrel(Anakin)  
Ask: Secret(_)  
Ask: Resource(_)  
True: Resource(Pine)  
True: Secret(Pine)  
Ask: Tells(Anakin, Pine, _)  
Ask: Resource(Pine)  
True: Resource(Pine)  
Ask: Knows(Sidious, Pine)  
True: Knows(Sidious, Pine)  
True: Tells(Anakin, Pine, Sidious)  
Ask: Hostile(Sidious)  
Ask: Enemy(Sidious, USC)  
True: Enemy(Sidious, USC)  
True: Hostile(Sidious)  
True: Traitor(Anakin)  
True 
