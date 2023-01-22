import os

from .. import exceptions, utils
from . import base

__all__ = ("TypeScript",)


class TypeScript(base.BaseCompiler):

    name = "typescript"
    input_extension = "ts"
    output_extension = "js"

    def __init__(self, tsc_executable="tsc", node_executable="", sourcemap_enabled=False, **kwargs):
        self.tsc_executable = tsc_executable
        self.node_executable = node_executable
        self.is_sourcemap_enabled = sourcemap_enabled
        self.kwargs = kwargs
        super(TypeScript, self).__init__()

    def compile_file(self, source_path):
        full_output_path = self.get_full_output_path(source_path)
        args = [
            self.node_executable,
            self.tsc_executable
        ]
        if self.kwargs:
            for k, v in self.kwargs.items():
                args.append(k)
                if v:
                    args.append(v)
            #args.extend([f"{k}", "{v}" if v else f"{k}" for k, v in self.kwargs.items()])
        if self.is_sourcemap_enabled:
            args.append("--sourceMap")
        args.extend(
            [
                "--outDir",
                os.path.dirname(full_output_path),
                self.get_full_source_path(source_path),
            ]
        )
        #print(args)
        return_code, out, errors = utils.run_command(args)

        if return_code:
            raise exceptions.StaticCompilationError(errors if errors else out)

        return self.get_output_path(source_path)

    def compile_source(self, source):
        raise NotImplementedError
