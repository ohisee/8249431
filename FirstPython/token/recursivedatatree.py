# Rama's Journey

# Suppose we input "Rama's Journey" to our parser. Define a variable ptree that
# holds the parse tree for this input.

ptree = [("word-element", "Rama's"), ("word-element","Journey")] # Change this variable!


def insert(tree, element):
    if tree == None:
        return (None, element, None);
    else:
        left_child = tree[0];
        this_element = tree[1];
        right_child = tree[2];
        if element <= this_element:
            new_left_child = insert(left_child, element);
            return (new_left_child, this_element, right_child);
        else:
            new_right_child = insert(right_child, element);
            return (left_child, this_element, new_right_child);
        
def print_tree(tree):
    if tree == None:
        return;
    else:
        left_child = tree[0];
        this_element = tree[1];
        right_child = tree[2];
        print_tree(left_child);
        print this_element;
        print_tree(right_child);
        
        