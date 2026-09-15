namespace IncidentCopilot;

internal static class Repo
{
    public static string FindRoot()
    {
        foreach (var start in new[]
        {
            new DirectoryInfo(Directory.GetCurrentDirectory()),
            new DirectoryInfo(AppContext.BaseDirectory),
        })
        {
            for (var dir = start; dir != null; dir = dir.Parent)
            {
                var runbooks = Path.Combine(dir.FullName, "runbooks");
                var samples = Path.Combine(dir.FullName, "samples");
                if (Directory.Exists(runbooks) && Directory.Exists(samples))
                    return dir.FullName;
            }
        }

        throw new DirectoryNotFoundException(
            "Could not find the repository root (looked for runbooks/ and samples/).");
    }

    public static string ResolveIncidentPath(string raw, string root)
    {
        if (Path.IsPathRooted(raw) && File.Exists(raw))
            return Path.GetFullPath(raw);

        var cwdPath = Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), raw));
        if (File.Exists(cwdPath))
            return cwdPath;

        return Path.GetFullPath(Path.Combine(root, raw));
    }

    public static string LoadIncident(string path)
    {
        if (!File.Exists(path))
            throw new FileNotFoundException($"incident file not found: {path}");
        var text = File.ReadAllText(path);
        if (string.IsNullOrWhiteSpace(text))
            throw new InvalidDataException($"Incident file is empty: {path}");
        return text;
    }

    public static string ExtractIncidentId(string text)
    {
        foreach (var raw in text.Split('\n'))
        {
            var line = raw.Trim();
            if (line.StartsWith("Ticket Number:", StringComparison.OrdinalIgnoreCase))
            {
                var value = line.Split(':', 2)[1].Trim();
                return string.IsNullOrEmpty(value) ? "unknown" : value;
            }
        }

        return "unknown";
    }
}
