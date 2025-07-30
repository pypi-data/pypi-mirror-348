import json
def viewDict(data):
    return JsonTree(data).view()
class JsonTree:
    def __init__(self, data):
        self.data = data
        self.root = JsonNode(data)

    def view(self, dictCollapse: bool = False, listCollapse: bool = True):
        return self.root.view(dictCollapse=dictCollapse, listCollapse=listCollapse)


class JsonNode:
    def __init__(self, data, depth: int = 0, autoInit: bool = True):
        self.depth = depth

        self.type = type(data).__name__
        if self.type == 'dict':
            self.children = {}
        elif self.type == 'list':
            self.children = []
        else:
            self.children = None
            return
        if autoInit:
            self.init(data)

    def init(self, data):
        if self.type == 'dict':
            for k in data.keys():
                self.children[k] = JsonNode(data[k], self.depth + 1, True)
        elif self.type == 'list':
            for v in data:
                self.children.append(JsonNode(v, self.depth + 1, True))
        else:
            raise Exception("Impossible")

    def __str__(self):
        return f"JsonNode(type={self.type},depth={self.depth})"

    def _view(self, info):
        return '\t' * self.depth + str(self.depth) + " " + info + "\n"

    def view(self, dictCollapse: bool, listCollapse: bool):
        ans = ""
        if self.type == 'dict':
            ans += self._view(f"{self.type} len={len(self.children.keys())}")
            if dictCollapse:
                tempTreeView = {}
                for k in self.children.keys():
                    tempTreeView[k] = self.children[k].view(dictCollapse=dictCollapse, listCollapse=listCollapse)

                selectedTreeView = {}

                for t in tempTreeView.keys():
                    if tempTreeView[t] not in selectedTreeView:
                        selectedTreeView[tempTreeView[t]] = [t]
                    else:
                        selectedTreeView[tempTreeView[t]].append(t)
                for t in selectedTreeView:
                    ans += self._view("Keys: " + str(selectedTreeView[t]))
                    ans += t
            else:
                for k in self.children.keys():
                    ans += self._view(f"Key: {k}")
                    ans += self.children[k].view(dictCollapse=dictCollapse, listCollapse=listCollapse)
        elif self.type == 'list':
            ans += self._view(f"{self.type} len={len(self.children)}")
            templistView = []
            if listCollapse:
                for v in self.children:
                    templistView.append(v.view(dictCollapse=dictCollapse, listCollapse=listCollapse))
                selectedlistView = {}
                for t in templistView:
                    if t not in selectedlistView:
                        selectedlistView[t] = 1
                    else:
                        selectedlistView[t] += 1
                for t in selectedlistView:
                    ans += self._view("Items Count: " + str(selectedlistView[t]))
                    ans += t
            else:
                for v in self.children:
                    ans += self._view('item:')
                    ans += v.view(dictCollapse=dictCollapse, listCollapse=listCollapse)
        else:
            ans += self._view(self.type)
        return ans

    def __eq__(self, other):
        if type(other) != JsonNode:
            return False
        return self.view() == other.view()


if __name__ == '__main__':
    """
    使用方法：加载一个json对象，然后JsonTree(该对象).view()即可
    """
    a = {"a": 1, "b": 2, "c": 3}
    # print(analyze(a, 0,True))
    tree = JsonTree(a)
    print(tree.view())