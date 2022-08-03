import checkers_utiles


class Node:
    def __init__(self, data=None, x=None, y=None):
        #self.data = data
        self.x = x
        self.y = y
        self.left = None
        self.right = None
        self.next = None


class BinaryTree:
    def __init__(self, data=None, x=None, y=None):
        self.root = Node(data, x, y)

    @classmethod
    def getLeafCount(cls, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        else:
            return cls.getLeafCount(node.left) + cls.getLeafCount(node.right)

    @classmethod
    def isIndexInLeaf(cls, node, target_x, target_y):
        if node is None:
            return False
        if node.left is None and node.right is None:
            if node.x == target_x and node.y == target_y:
                return True
            else:
                return False
        else:
            return cls.isIndexInLeaf(node.left, target_x, target_y) or cls.isIndexInLeaf(node.right, target_x, target_y)

    @classmethod
    def nodesToTargetLeaf(cls, node, target_x, target_y):
        """
        :param node: root node
        :param target_x: target index x
        :param target_y: target index y
        :return: "True" if target index (x,y) exist, and it's node is a leaf.
        The function also set "node.next" to enable path to that target leaf.
        """
        if node is None:
            return False

        # if node is a leaf:
        if node.left is None and node.right is None:
            if node.x == target_x and node.y == target_y:
                return True
            else:
                return False
        else:
            ans_left = cls.nodesToTargetLeaf(node.left, target_x, target_y)
            ans_right = cls.nodesToTargetLeaf(node.right, target_x, target_y)
            if ans_left:
                node.next = node.left
                return ans_left
            elif ans_right:
                node.next = node.right
                return ans_right
            else:
                return False

    @classmethod
    def maxDepth(cls, node):
        if node is None:
            return -1
        else:
            # Compute the depth of each subtree
            lDepth = cls.maxDepth(node.left)
            rDepth = cls.maxDepth(node.right)

            # Use the larger one
            if lDepth > rDepth:
                return lDepth + 1
            else:
                return rDepth + 1




'''
# Driver program to test above function
root = BinaryTree(data=11, x=1, y=2)
root.left = Node(data=12, x=3, y=4)
root.right = Node(data=13, x=5, y=6)
root.left.left = Node(data=14, x=7, y=8)
root.left.right = Node(data=15, x=9, y=2)
root.right.left = Node(data=16, x=6, y=5)
root.right.right = Node(data=17, x=4, y=9)

print(f"Leaf count of the tree is {root.getLeafCount(root)}")

for val in range(11, 18):
    print(f"is {val} In Leaf? {root.isValueInLeaf(root, val)}")

ind_x = 4
ind_y = 9
print(f"is x={ind_x} y={ind_y} in Leaf? {root.isIndexInLeaf(root, ind_x, ind_y)}")
'''


'''
def chainer(node):
    if node.data != 0:
        new_node = Node(data=node.data - 1)
        node.left = new_node
        chainer(new_node)


tree = BinaryTree(data=3, x=1, y=1)
chainer(tree.root)
print(tree.root.data)
print(tree.root.left.data)
print(tree.root.left.left.data)
print(tree.root.left.left.left.data)
print(tree.root.left.left.left.left)
'''


def chainCaptures(node, player, board_state):
    # chain to the left:
    x1 = node.x + 2 * player
    y1 = node.y + 2 * player
    if checkers_utiles.validate_single_capture(player=player, x0=node.x, y0=node.y, x1=x1, y1=y1, board_state=board_state):
        new_node = Node(x=x1, y=y1)
        node.left = new_node
        chainCaptures(node=new_node, player=player, board_state=board_state)

    # chain to the right:
    x1 = node.x - 2 * player
    y1 = node.y + 2 * player
    if checkers_utiles.validate_single_capture(player=player, x0=node.x, y0=node.y, x1=x1, y1=y1, board_state=board_state):
        new_node = Node(x=x1, y=y1)
        node.right = new_node
        chainCaptures(node=new_node, player=player, board_state=board_state)



if __name__ == '__main__':
    print(f"Start run binary tree....")
    state_2 = [
        [0,  1,  0,  1,  0,  1,  0, 1],
        [1,  0,  1,  0,  1,  0,  1, 0],
        [0, -1,  0,  1,  0,  1,  0, 1],
        [0,  0,  0,  0, -1,  0,  0, 0],
        [0,  0,  0, -1,  0,  0,  0, 0],
        [-1, 0, -1,  0, -1,  0, -1, 0],
        [0, -1,  0,  0,  0, -1,  0, 0],
        [-1, 0, -1,  0, -1,  0, -1, 0],
    ]

    #tree = BinaryTree(x=3, y=2)
    tree = BinaryTree(x=0, y=0)
    chainCaptures(tree.root, player=1, board_state=state_2)

    '''
    print(f"node_0   X,Y = {tree.root.x},{tree.root.y}")
    print(f"node_1   X,Y = {tree.root.left.x},{tree.root.left.y}")
    print(f"node_2   X,Y = {tree.root.left.left.x},{tree.root.left.left.y}")
    '''

    ind_x = 3
    ind_y = 6
    print(f"is x={ind_x} y={ind_y} in Leaf? {tree.isIndexInLeaf(tree.root, ind_x, ind_y)}")

    tree_depth = tree.maxDepth(tree.root)
    print(f"Max depth: {tree_depth}")

    ans = tree.nodesToTargetLeaf(tree.root, ind_x, ind_y)

    while_node = tree.root
    while while_node:
        print(f"node   X,Y = {while_node.x},{while_node.y}")
        while_node = while_node.next


    z = 770

