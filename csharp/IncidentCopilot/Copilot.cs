using System.Text.Json;
using System.Text.Json.Serialization;

namespace IncidentCopilot;

internal sealed record CopilotResult(IReadOnlyList<Hit> Hits, string Answer, double LatencySeconds, string Model);

internal sealed class CopilotLog
{
    [JsonPropertyName("timestamp")]
    public string Timestamp { get; set; } = "";

    [JsonPropertyName("incident_id")]
    public string IncidentId { get; set; } = "";

    [JsonPropertyName("incident_file")]
    public string IncidentFile { get; set; } = "";

    [JsonPropertyName("chunks_used")]
    public List<ChunkLog> ChunksUsed { get; set; } = [];

    [JsonPropertyName("model")]
    public string Model { get; set; } = "";

    [JsonPropertyName("answer")]
    public string Answer { get; set; } = "";

    [JsonPropertyName("latency_s")]
    public double LatencyS { get; set; }
}

internal sealed class ChunkLog
{
    [JsonPropertyName("name")]
    public string Name { get; set; } = "";

    [JsonPropertyName("heading")]
    public string Heading { get; set; } = "";

    [JsonPropertyName("score")]
    public double Score { get; set; }
}

internal static class Copilot
{
    public static async Task<CopilotResult> RunAsync(string incidentText, string repoRoot, int k = 3)
    {
        var runbooks = Retrieval.LoadRunbooks(repoRoot);
        var chunks = Retrieval.ChunkRunbooks(runbooks);
        var hits = Retrieval.Retrieve(incidentText, chunks, k);
        var (answer, latency) = await GrokClient.AskAsync(incidentText, hits, repoRoot);
        return new CopilotResult(hits, answer, latency, GrokClient.Model);
    }

    public static string AppendJsonl(string repoRoot, CopilotLog record)
    {
        var dir = Path.Combine(repoRoot, "logs");
        Directory.CreateDirectory(dir);
        var path = Path.Combine(dir, "copilot.jsonl");
        var line = JsonSerializer.Serialize(record);
        File.AppendAllText(path, line + Environment.NewLine);
        return path;
    }
}
