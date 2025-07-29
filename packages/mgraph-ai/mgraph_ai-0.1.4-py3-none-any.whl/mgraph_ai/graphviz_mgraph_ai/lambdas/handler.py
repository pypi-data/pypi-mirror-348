from mangum                                              import Mangum
from osbot_utils.utils.Env                               import get_env
from mgraph_ai_serverless.fast_api.MGraph_AI_Serverless__Fast_API import MGraph_AI_Serverless__Fast_API

fast_api__mgraph_ai_serverless = MGraph_AI_Serverless__Fast_API().setup()
app                  = fast_api__mgraph_ai_serverless.app()
run                  = Mangum(app)

if __name__ == "__main__":                              # pragma: no cover
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)