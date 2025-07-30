from pathlib import Path


def generate_file(log, output_file, commit_output, pr_output=None, skip_summary=False):
    try:
        if isinstance(commit_output, list):
            commit_output = "\n".join(commit_output)
        if isinstance(pr_output, list):
            pr_output = "\n".join(pr_output)

        commit_lines = [line.strip() for line in commit_output.strip().splitlines() if line.strip()]
        pr_lines = [line.strip() for line in pr_output.strip().splitlines() if line.strip()] if pr_output else []

        combined_messages = []
        for line in commit_lines:
            parts = line.split("|", 3)
            if len(parts) == 4:
                author = parts[1].strip()
                message = parts[3].strip()
                combined_messages.append(f"{author} - {message}")

        summary = ""
        if not skip_summary and combined_messages:
            try:
                from git_log_stat.git_repo.git_nlp import init_summarizer
                summarizer = init_summarizer()
                full_text = ". ".join(combined_messages)
                full_text = " ".join(full_text.split()[:1024])
                summary = summarizer(full_text, max_length=120, min_length=40, do_sample=False)[0]['summary_text']
            except ImportError:
                log.warning("⚠️ Summarizer module not found. Skipping summary.")
            except Exception as e:
                log.warning(f"⚠️ Summarization failed: {e}")

        out_file_path = Path(output_file).resolve()
        with open(out_file_path, 'w', encoding='utf-8') as out_file:
            if summary:
                out_file.write("📝 Summary:\n")
                out_file.write(summary + "\n\n")

            out_file.write("📜 Commits:\n")
            for line in commit_lines:
                out_file.write(line + "\n")
            out_file.write("\n")

            if pr_lines:
                out_file.write("🔀 Pull Requests:\n")
                for line in pr_lines:
                    out_file.write(line + "\n")

        log.info(f"✅ Text file written to: {out_file_path}")

    except Exception as e:
        log.error(f"❌ Failed to write text file: {e}", exc_info=True)