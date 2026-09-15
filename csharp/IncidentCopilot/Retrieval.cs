using System.Text.RegularExpressions;

namespace IncidentCopilot;

internal sealed record Runbook(string Name, string Text);

internal sealed record Chunk(string Name, string Heading, string Text);

internal sealed record Hit(string Name, string Heading, string Text, double Score);

internal static class Retrieval
{
    private static readonly Regex Token = new("[a-z0-9]+", RegexOptions.Compiled);
    private static readonly HashSet<string> Stopwords = new(StringComparer.Ordinal)
    {
        "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to", "for",
        "of", "as", "is", "are", "was", "were", "be", "been", "being", "by", "with",
        "from", "this", "that", "these", "those", "it", "its", "we", "you", "your",
        "not", "no", "do", "does", "did", "can", "could", "should", "would",
    };

    public static List<Runbook> LoadRunbooks(string root)
    {
        var dir = Path.Combine(root, "runbooks");
        if (!Directory.Exists(dir))
            throw new DirectoryNotFoundException($"runbooks folder not found: {dir}");

        var loaded = new List<Runbook>();
        foreach (var path in Directory.GetFiles(dir, "*.md").OrderBy(p => p, StringComparer.Ordinal))
        {
            var text = File.ReadAllText(path);
            if (string.IsNullOrWhiteSpace(text))
                continue;
            loaded.Add(new Runbook(Path.GetFileName(path), text));
        }

        if (loaded.Count == 0)
            throw new InvalidDataException($"no runbook markdown files in {dir}");
        return loaded;
    }

    public static List<Chunk> ChunkRunbooks(IEnumerable<Runbook> runbooks)
    {
        var chunks = new List<Chunk>();
        foreach (var book in runbooks)
        {
            var heading = book.Name;
            var lines = new List<string>();
            foreach (var line in book.Text.Split('\n'))
            {
                var raw = line.TrimEnd('\r');
                if (raw.StartsWith("## ", StringComparison.Ordinal))
                {
                    Flush(chunks, book.Name, heading, lines);
                    heading = raw[3..].Trim();
                    lines = [raw];
                }
                else
                {
                    lines.Add(raw);
                }
            }

            Flush(chunks, book.Name, heading, lines);
        }

        return chunks;
    }

    public static List<Hit> Retrieve(string incidentText, IReadOnlyList<Chunk> chunks, int k = 3)
    {
        if (chunks.Count == 0)
            return [];

        var docs = chunks.Select(c => Tokenize(c.Text)).ToList();
        var query = Tokenize(incidentText);
        var df = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var doc in docs)
        {
            foreach (var term in doc.Keys)
                df[term] = df.GetValueOrDefault(term) + 1;
        }

        var n = docs.Count;
        var queryVec = TfIdf(query, df, n);
        var scored = new List<(double Score, Chunk Chunk)>(n);
        for (var i = 0; i < n; i++)
        {
            var docVec = TfIdf(docs[i], df, n);
            scored.Add((Cosine(queryVec, docVec), chunks[i]));
        }

        return scored
            .OrderByDescending(s => s.Score)
            .Take(k)
            .Select(s => new Hit(s.Chunk.Name, s.Chunk.Heading, s.Chunk.Text, s.Score))
            .ToList();
    }

    private static void Flush(List<Chunk> chunks, string name, string heading, List<string> lines)
    {
        var text = string.Join('\n', lines).Trim();
        if (text.Length > 0)
            chunks.Add(new Chunk(name, heading, text));
    }

    private static Dictionary<string, int> Tokenize(string text)
    {
        var counts = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (Match match in Token.Matches(text.ToLowerInvariant()))
        {
            var term = match.Value;
            if (term.Length < 2 || Stopwords.Contains(term))
                continue;
            counts[term] = counts.GetValueOrDefault(term) + 1;
        }

        return counts;
    }

    private static Dictionary<string, double> TfIdf(
        Dictionary<string, int> tf,
        Dictionary<string, int> df,
        int n)
    {
        var vec = new Dictionary<string, double>(StringComparer.Ordinal);
        foreach (var (term, count) in tf)
        {
            if (!df.TryGetValue(term, out var docsWithTerm))
                continue;
            var idf = Math.Log((n + 1.0) / (docsWithTerm + 1.0)) + 1.0;
            vec[term] = count * idf;
        }

        return vec;
    }

    private static double Cosine(Dictionary<string, double> a, Dictionary<string, double> b)
    {
        double dot = 0, na = 0, nb = 0;
        foreach (var v in a.Values)
            na += v * v;
        foreach (var v in b.Values)
            nb += v * v;
        if (na == 0 || nb == 0)
            return 0;
        foreach (var (term, av) in a)
        {
            if (b.TryGetValue(term, out var bv))
                dot += av * bv;
        }

        return dot / (Math.Sqrt(na) * Math.Sqrt(nb));
    }
}
