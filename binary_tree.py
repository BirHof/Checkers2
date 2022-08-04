import checkers_utiles


class Node:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.left = None
        self.right = None
        self.next = None


class BinaryTree:
    def __init__(self, x=None, y=None):
        self.root = Node(x, y)

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

