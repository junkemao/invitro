package function

import (
	"context"
	tc "github.com/eth-easl/loader/pkg/common"
	"time"

	log "github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	"go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"

	util "github.com/eth-easl/loader/pkg"
	mc "github.com/eth-easl/loader/pkg/metric"
	"github.com/eth-easl/loader/server"
)

const (
	functionPort = ":80"

	// TODO: figure out the meaning of the contexts associated with this
	// TODO: change the values and make them configurable from outside
	grpcConnectionTimeout = 1 * time.Minute
	// Function can execute for at most 15 minutes as in AWS Lambda
	// https://aws.amazon.com/about-aws/whats-new/2018/10/aws-lambda-supports-functions-that-can-run-up-to-15-minutes/
	functionTimeout = 15 * time.Minute
)

func Invoke(function tc.Function, runtimeSpec *tc.RuntimeSpecification, withTracing bool) (bool, mc.ExecutionRecord) {
	log.Tracef("(Invoke)\t %s: %d[ms], %d[MiB]", function.Name, runtimeSpec.Runtime, runtimeSpec.Memory)

	var record mc.ExecutionRecord

	record.FuncName = function.Name
	record.RequestedDuration = uint32(runtimeSpec.Runtime * 1e3)

	////////////////////////////////////
	// INVOKE FUNCTION
	////////////////////////////////////
	start := time.Now()
	record.StartTime = start.UnixMicro()

	// TODO: a gRPC pool may come in handy here
	dialContext, cancelDialing := context.WithTimeout(context.Background(), grpcConnectionTimeout)
	defer cancelDialing()

	var dialOptions []grpc.DialOption
	dialOptions = append(dialOptions, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if withTracing {
		// NOTE: if enabled it will exclude Istio span from the Zipkin trace
		dialOptions = append(dialOptions, grpc.WithUnaryInterceptor(otelgrpc.UnaryClientInterceptor()))
	}

	conn, err := grpc.DialContext(dialContext, function.Endpoint+functionPort, dialOptions...)
	defer closeConn(conn)
	if err != nil {
		log.Warnf("Failed to establish a gRPC connection - %v\n", err)

		record.ResponseTime = time.Since(start).Microseconds()
		record.ConnectionTimeout = false

		return false, record
	}

	grpcClient := server.NewExecutorClient(conn)

	// Contact the server and print out its response.
	executionCxt, cancelExecution := context.WithTimeout(context.Background(), functionTimeout)
	defer cancelExecution()

	response, err := grpcClient.Execute(executionCxt, &server.FaasRequest{
		Message:           "nothing",
		RuntimeInMilliSec: uint32(runtimeSpec.Runtime),
		MemoryInMebiBytes: uint32(runtimeSpec.Memory),
	})

	if err != nil {
		log.Warnf("Failed  in gRPC execution (%s): %v", function.Name, err)

		record.ResponseTime = time.Since(start).Microseconds()
		record.FunctionTimeout = true

		return false, record
	}

	record.ResponseTime = time.Since(start).Microseconds()
	record.ActualDuration = response.DurationInMicroSec

	log.Tracef("(Replied)\t %s: %s, %.2f[ms], %d[MiB]", function.Name, response.Message,
		float64(response.DurationInMicroSec)/1e3, util.Kib2Mib(0))
	log.Tracef("(E2E Latency) %s: %.2f[ms]\n", function.Name, float64(record.ResponseTime)/1e3)

	return true, record
}
