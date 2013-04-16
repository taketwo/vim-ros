let g:xmldata_roslaunch = {
\ 'vimxmlentities': [],
\ 'vimxmlroot': ['launch'],
\ 'launch': [
    \ ['node', 'param', 'remap', 'machine', 'rosparam', 'include', 'env', 'test', 'arg'],
    \ {'deprecated': []}
\ ],
\ 'node': [
    \ ['arg', 'remap'],
    \ {'pkg': [],
    \  'type': [],
    \  'name': [],
    \  'args': []}
\ ],
\ 'vimxmlattrinfo' : {
\ 'pkg': ['Package of node', 'Package of node.'],
\ 'type': ['Node type', 'Node type. There must be a corresponding executable with the same name.'],
\ 'name': ['Node name', 'Node name. Note: name cannot contain a namespace. Use the ns attribute instead.'],
\ 'args': ['Pass arguments to node', 'Pass arguments to node (optional).']
\ },
\ 'vimxmltaginfo': {
\ 'node': ['ROS node', 'The <node> tag specifies a ROS node that you wish to have launched. This is the most common roslaunch tag as it supports the most important features: bringing up and taking down nodes. roslaunch does not provide any guarantees about what order nodes start in. This is intentional: there is no way to externally know when a node is fully initialized, so all code that is launched must be robust to launching in any order.'],
\ }
\ }
