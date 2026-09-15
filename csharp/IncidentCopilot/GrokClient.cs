using System.Diagnostics;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace IncidentCopilot;

internal static class GrokClient
{
    public const string Model = "grok-4.6";
    public const string SystemPrompt = """
        You are an application-support copilot for a banking portal.

        Rules:
        - Use ONLY the runbook excerpts in the user message.
        - Cite the runbook filename (for example sql_timeout.md) on each recommended step.
        - If the runbooks do not cover the issue, say you do not know. Do not invent procedures.
        - Do not ask for PAN, SSN, passwords, or full customer records.
        - Output short numbered diagnostic next steps. No preamble.
        """;

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
    };

    public static async Task<(string Answer, double LatencySeconds)> AskAsync(
        string incidentText,
        IReadOnlyList<Hit> hits,
        string repoRoot)
    {
        var apiKey = Environment.GetEnvironmentVariable("XAI_API_KEY");
        if (string.IsNullOrWhiteSpace(apiKey))
        {
            throw new InvalidOperationException(
                "XAI_API_KEY is missing.\n" +
                $"Put one line in {Path.Combine(repoRoot, ".env")}:\n" +
                "XAI_API_KEY=your_key_here");
        }

        var userMessage = FormatUserMessage(incidentText, hits);
        var body = new ChatRequest
        {
            Model = Model,
            Messages =
            [
                new ChatMessage { Role = "system", Content = SystemPrompt },
                new ChatMessage { Role = "user", Content = userMessage },
            ],
        };

        using var http = new HttpClient { Timeout = TimeSpan.FromMinutes(2) };
        using var request = new HttpRequestMessage(HttpMethod.Post, "https://api.x.ai/v1/chat/completions");
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
        request.Content = new StringContent(JsonSerializer.Serialize(body, JsonOptions), Encoding.UTF8, "application/json");

        var started = Stopwatch.StartNew();
        using var response = await http.SendAsync(request);
        var raw = await response.Content.ReadAsStringAsync();
        started.Stop();
        if (!response.IsSuccessStatusCode)
            throw new HttpRequestException($"Grok HTTP {(int)response.StatusCode}: {raw}");

        var parsed = JsonSerializer.Deserialize<ChatResponse>(raw, JsonOptions);
        var answer = parsed?.Choices?.FirstOrDefault()?.Message?.Content?.Trim();
        if (string.IsNullOrEmpty(answer))
            throw new InvalidOperationException("Grok returned an empty answer");
        return (answer, started.Elapsed.TotalSeconds);
    }

    public static string FormatUserMessage(string incidentText, IReadOnlyList<Hit> hits)
    {
        var parts = new List<string> { "Incident:", incidentText.Trim(), "", "Runbook excerpts:" };
        for (var i = 0; i < hits.Count; i++)
        {
            var hit = hits[i];
            parts.Add($"--- [{i + 1}] {hit.Name} / {hit.Heading} ---");
            parts.Add(hit.Text.Trim());
            parts.Add("");
        }

        return string.Join('\n', parts);
    }

    private sealed class ChatRequest
    {
        public string Model { get; set; } = "";
        public List<ChatMessage> Messages { get; set; } = [];
    }

    private sealed class ChatMessage
    {
        public string Role { get; set; } = "";
        public string Content { get; set; } = "";
    }

    private sealed class ChatResponse
    {
        public List<ChatChoice>? Choices { get; set; }
    }

    private sealed class ChatChoice
    {
        public ChatMessage? Message { get; set; }
    }
}
