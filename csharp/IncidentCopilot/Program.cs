namespace IncidentCopilot;

internal static class Program
{
    public static async Task<int> Main(string[] args)
    {
        string? incidentArg = null;
        for (var i = 0; i < args.Length; i++)
        {
            if (args[i] == "--incident" && i + 1 < args.Length)
            {
                incidentArg = args[i + 1];
                break;
            }
        }

        if (string.IsNullOrWhiteSpace(incidentArg))
        {
            Console.Error.WriteLine("Usage: dotnet run --project csharp/IncidentCopilot -- --incident samples/sql_timeout.txt");
            return 1;
        }

        try
        {
            return await RunAsync(incidentArg);
        }
        catch (Exception ex) when (ex is InvalidOperationException or FileNotFoundException
                                       or DirectoryNotFoundException or InvalidDataException
                                       or HttpRequestException)
        {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
    }

    private static async Task<int> RunAsync(string incidentArg)
    {
        var repoRoot = Repo.FindRoot();
        DotEnv.Load(Path.Combine(repoRoot, ".env"));

        var path = Repo.ResolveIncidentPath(incidentArg, repoRoot);
        var text = Repo.LoadIncident(path);
        var ticketId = Repo.ExtractIncidentId(text);

        Console.WriteLine($"Incident ID: {ticketId}");
        Console.WriteLine($"File: {path}");
        Console.WriteLine();
        Console.WriteLine(text);

        var result = await Copilot.RunAsync(text, repoRoot, k: 3);

        Console.WriteLine();
        Console.WriteLine("Retrieved:");
        foreach (var hit in result.Hits)
            Console.WriteLine($"  {hit.Name} / {hit.Heading}  {Math.Round(hit.Score, 3)}");

        Console.WriteLine();
        Console.WriteLine($"Model: {result.Model}  latency: {result.LatencySeconds:F3}s");
        Console.WriteLine();
        Console.WriteLine(result.Answer);

        var logPath = Copilot.AppendJsonl(repoRoot, new CopilotLog
        {
            Timestamp = DateTimeOffset.UtcNow.ToString("o"),
            IncidentId = ticketId,
            IncidentFile = path,
            ChunksUsed = result.Hits.Select(h => new ChunkLog
            {
                Name = h.Name,
                Heading = h.Heading,
                Score = h.Score,
            }).ToList(),
            Model = result.Model,
            Answer = result.Answer,
            LatencyS = Math.Round(result.LatencySeconds, 3),
        });

        Console.WriteLine();
        Console.WriteLine($"Logged: {logPath}");
        return 0;
    }
}
