
# use dfs to detect circular dependencies in the task dependency graph
# graph = { all taks id : dependencies list}, directed from id to dependencies

# recursive approach
def check_circular_dependencies(task_graph):
    seen = set()
    current_path = []

    def visit(node):
        if node in current_path: # nodes are each task id, if we see a node in the current path, we have a cycle
          
            culprit = node
            cycle_path = current_path[current_path.index(node):] + [node]
            return {"has_cycle": True, "culprit": culprit, "cycle": cycle_path}
        
        if node in seen: # if we have already visited this node and it is not in the current path, then we can skip it
            return {"has_cycle": False}

        current_path.append(node)
        seen.add(node)

        for neighbor in task_graph.get(node, []): # neighbors = dependencies of the current node
            result = visit(neighbor)
            if result["has_cycle"]:
                return result

        current_path.pop()
        return {"has_cycle": False}

    for node in task_graph:
        if node not in seen:
            result = visit(node)
            if result["has_cycle"]:
                return result
    return {"has_cycle": False}

def check_self_dependency(task_id, dependencies):
    if task_id in dependencies:
        raise ValueError(f"Task with ID {task_id} cannot depend on itself.")