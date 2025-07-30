import argparse
from argparse import ArgumentParser, Namespace
from typing import Optional

from dtx.core.models.evaluator import (
    AnyJsonPathExpBasedPromptEvaluation,
    AnyKeywordBasedPromptEvaluation,
    EvaluationModelName,
    EvaluationModelType,
    EvaluatorInScope,
    ModelBasedPromptEvaluation,
)


class EvalMethodArgs:
    """
    Handles argument parsing and creation of EvaluatorInScope based on simple --eval input.
    """

    # Mapping of eval to model name, type, and required env variables
    EVAL_CHOICES = {
        "any": {
            "model_name": EvaluationModelName.ANY,
            "model_type": EvaluationModelType.TOXICITY,
            "env_vars": [],
        },
        "keyword": {
            "model_name": EvaluationModelName.ANY_KEYWORD_MATCH,
            "model_type": EvaluationModelType.STRING_SEARCH,
            "env_vars": [],
        },
        "jsonpath": {
            "model_name": EvaluationModelName.ANY_JSONPATH_EXP,
            "model_type": EvaluationModelType.JSON_EXPRESSION,
            "env_vars": [],
        },
        "ibm": {
            "model_name": EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_125M,
            "model_type": EvaluationModelType.TOXICITY,
            "env_vars": [],
        },
        "ibm38": {
            "model_name": EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_38M,
            "model_type": EvaluationModelType.TOXICITY,
            "env_vars": [],
        },
        "ibm125": {
            "model_name": EvaluationModelName.IBM_GRANITE_TOXICITY_HAP_125M,
            "model_type": EvaluationModelType.TOXICITY,
            "env_vars": [],
        },
        "openai": {
            "model_name": EvaluationModelName.POLICY_BASED_EVALUATION_OPENAI,
            "model_type": EvaluationModelType.POLICY,
            "env_vars": ["OPENAI_API_KEY"],
        },
        "ollama": {
            "model_name": EvaluationModelName.OLLAMA_LLAMA_GUARD,
            "model_type": EvaluationModelType.TOXICITY,
            "env_vars": [],
        },
        "llamaguard": {
            "model_name": EvaluationModelName.OLLAMA_LLAMA_GUARD,
            "model_type": EvaluationModelType.TOXICITY,
            "env_vars": [],
        },
    }

    def _format_help_message(self) -> str:
        # Group types for prettier help formatting
        groupings = {
            "🧩 Toxicity Models": [],
            "🔍 Keyword Search": [],
            "🗂️ JSONPath Expression": [],
            "🧠 Policy-Based": [],
        }

        for name, config in sorted(self.EVAL_CHOICES.items()):
            model_name = config["model_name"]
            model_type = config["model_type"]
            env_note = (
                f" (env: {', '.join(config['env_vars'])})" if config["env_vars"] else ""
            )
            line = f"  {name:<12} → {model_name.value}{env_note}"
            if model_type == EvaluationModelType.TOXICITY:
                groupings["🧩 Toxicity Models"].append(line)
            elif model_type == EvaluationModelType.STRING_SEARCH:
                groupings["🔍 Keyword Search"].append(line)
            elif model_type == EvaluationModelType.JSON_EXPRESSION:
                groupings["🗂️ JSONPath Expression"].append(line)
            elif model_type == EvaluationModelType.POLICY:
                groupings["🧠 Policy-Based"].append(line)

        # Build final help message
        help_message = "Evaluator Choices:\n"
        for title, lines in groupings.items():
            if lines:
                help_message += f"\n{title}:\n" + "\n".join(lines) + "\n"

        return help_message

    def augment_args(self, parser: ArgumentParser):
        """Add evaluator arguments to the parser."""
        parser.add_argument(
            "--eval",
            choices=list(self.EVAL_CHOICES.keys()),
            metavar="EVALUATOR",
            help=self._format_help_message(),
        )
        parser.add_argument(
            "--keywords",
            nargs="*",
            metavar="KEYWORD",
            help="Keywords for keyword-based evaluation (required if --eval=keyword).",
        )
        parser.add_argument(
            "--expressions",
            nargs="*",
            metavar="EXPRESSION",
            help="JSONPath expressions for expression-based evaluation (required if --eval=jsonpath).",
        )

    def parse_args(
        self, args: Namespace, parser: Optional[ArgumentParser] = None
    ) -> Optional[EvaluatorInScope]:
        """Parse provided args namespace and return EvaluatorInScope object or None."""
        parser = parser or argparse.ArgumentParser()

        eval_choice = args.eval
        if not eval_choice:
            return None  # No evaluator specified

        eval_choice = eval_choice.strip().lower()

        if eval_choice not in self.EVAL_CHOICES:
            valid = ", ".join(self.EVAL_CHOICES.keys())
            parser.error(
                f"❌ Invalid --eval choice '{eval_choice}'.\n✅ Valid options: {valid}"
            )

        config = self.EVAL_CHOICES[eval_choice]
        model_name = config["model_name"]
        model_type = config["model_type"]

        # ✅ Optional: Validate env vars for this eval type
        missing_envs = [var for var in config["env_vars"] if not os.getenv(var)]
        if missing_envs:
            parser.error(
                f"❌ Missing required environment variables for eval '{eval_choice}': {', '.join(missing_envs)}"
            )

        # Build evaluator
        if model_type == EvaluationModelType.STRING_SEARCH:
            if not args.keywords:
                parser.error("❌ --keywords is required when using --eval=keyword.")
            evaluator = AnyKeywordBasedPromptEvaluation(keywords=args.keywords)

        elif model_type == EvaluationModelType.JSON_EXPRESSION:
            if not args.expressions:
                parser.error("❌ --expressions is required when using --eval=jsonpath.")
            evaluator = AnyJsonPathExpBasedPromptEvaluation(
                expressions=args.expressions
            )

        else:
            evaluator = ModelBasedPromptEvaluation(
                eval_model_type=model_type,
                eval_model_name=model_name,
            )

        return EvaluatorInScope(evaluation_method=evaluator)


# === Main entry point ===
def main():
    parser = argparse.ArgumentParser(
        description="Create EvaluatorInScope configuration"
    )

    # Create instance of EvalMethodArgs and add arguments
    eval_args = EvalMethodArgs()
    eval_args.augment_args(parser)

    # Other arguments (like output file)
    parser.add_argument(
        "--output",
        help="Optional output path to save configuration as JSON.",
    )

    args = parser.parse_args()

    evaluator_scope = eval_args.parse_args(args, parser)

    if evaluator_scope:
        output_json = evaluator_scope.model_dump_json(indent=2)
        print(output_json)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output_json)
            print(f"\n✅ Configuration saved to {args.output}")
    else:
        print("No evaluator specified. Skipping evaluator creation.")


if __name__ == "__main__":
    main()
