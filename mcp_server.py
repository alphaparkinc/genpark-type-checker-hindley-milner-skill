import sys
import json
from client import HMTypeInference, TypeVar, TypeOperator

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-type-checker-hindley-milner-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "unify_types",
                    "description": "Unify two types and solve polymorphic type equations using Hindley-Milner",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "type_a": {"type": "string"},
                            "type_b": {"type": "string"}
                        },
                        "required": ["type_a", "type_b"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "unify_types":
            ta = args.get("type_a")
            tb = args.get("type_b")
            hm = HMTypeInference()
            var_t = TypeVar(ta)
            concrete = TypeOperator(tb, [])
            hm.unify(var_t, concrete)
            res = {"content": [{"type": "text", "text": json.dumps({"unified_type": repr(hm.prune(var_t)), "status": "success"})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
