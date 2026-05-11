using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using System.Reactive;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class BuildRegisteredMessage
{
    private AllenNeuralDynamics.AindBehaviorServices.MessageProtocol.MessageType messageType = AllenNeuralDynamics.AindBehaviorServices.MessageProtocol.MessageType.Event;
    public AllenNeuralDynamics.AindBehaviorServices.MessageProtocol.MessageType MessageType
    {
        get { return messageType; }
        set { messageType = value; }
    }

    private const int protocolVersion = 0;

    private string rigName;
    public string RigName
    {
        get { return rigName; }
        set { rigName = value; }
    }

    public IObservable<AindJustFramesSchemas.MessageProtocol.RegisteredMessages> Process(IObservable<AindJustFramesSchemas.MessageProtocol.RegisteredPayload> source)
    {
        return Process(source.Select(value => new Timestamped<AindJustFramesSchemas.MessageProtocol.RegisteredPayload>(value, DateTimeOffset.UtcNow)));
    }

    public IObservable<AindJustFramesSchemas.MessageProtocol.RegisteredMessages> Process(IObservable<Timestamped<AindJustFramesSchemas.MessageProtocol.RegisteredPayload>> source)
    {
        string hostname = Environment.MachineName;
        string processId = System.Diagnostics.Process.GetCurrentProcess().Id.ToString();
        return source.Select(value => new AindJustFramesSchemas.MessageProtocol.RegisteredMessages()
        {
            MessageType = MessageType,
            ProtocolVersion = protocolVersion,
            Timestamp = value.Timestamp,
            ProcessId = processId,
            Hostname = hostname,
            RigName = RigName,
            Payload = value.Value
        });
    }
}
