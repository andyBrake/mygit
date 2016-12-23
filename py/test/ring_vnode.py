

NODE_COUNT = 100
DATA_ID_COUNT = 10000000
VNODE_COUNT = 1000

vnode_range_starts = []
vnode2node = []
for vnode_id in xrange(VNODE_COUNT):
    vnode_range_starts.append(DATA_ID_COUNT /
                              VNODE_COUNT * vnode_id)
    vnode2node.append(vnode_id % NODE_COUNT)
new_vnode2node = list(vnode2node)

print('vnode2node :')
print(vnode2node)
print("new_vnode2node :")
print(new_vnode2node)

new_node_id = NODE_COUNT
NEW_NODE_COUNT = NODE_COUNT + 1
vnodes_to_reassign = VNODE_COUNT / NEW_NODE_COUNT

print("reassign : ", vnodes_to_reassign)

while vnodes_to_reassign > 0:
    print("while exec : ")
    for node_to_take_from in xrange(NODE_COUNT):
        for vnode_id, node_id in enumerate(new_vnode2node):
            if node_id == node_to_take_from:
                print("node_to_take_from:", node_to_take_from, " node_id:", node_id, " vnode_id:", vnode_id)
                new_vnode2node[vnode_id] = new_node_id
                vnodes_to_reassign -= 1
                if vnodes_to_reassign <= 0:
                    break
        if vnodes_to_reassign <= 0:
            break
print("atfer handle, new_vnode2node:")
print(new_vnode2node)
print("=================================")