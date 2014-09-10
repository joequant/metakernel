# Copyright (c) Calico Development Team.
# Distributed under the terms of the Modified BSD License.
# http://calicoproject.org/

from jupyter_kernel import Magic, option
import logging

class KernelMagic(Magic):
    kernels = {}

    def line_kernel(self, module_name, class_name, kernel_name="default"):
        """
        %kernel MODULE CLASS [NAME] - construct a kernel for sending code.

        Also returns the kernel as output.

        Example:

            %kernel bash_kernel BashKernel bash

        Use `%%kernel bash` to send code to the kernel.
        """
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        # FIXME: monkeypatch to replace methods of class
        #        with methods of instance
        class_.subkernel(self.kernel)
        self.kernels[kernel_name] = class_()
        self.retval = self.kernels[kernel_name]

    def cell_kernel(self, kernel_name="default"):
        """
        %%kernel [NAME] - send the cell code to the kernel.

        Returns the result of the execution as output.

        Example:

            %%kernel bash
            ls -al 

        Use `%kernel MODULE CLASS [NAME]` to create a kernel.
        """
        self.retval = self.kernels[kernel_name].do_execute_direct(self.code)
        self.evaluate = False

    def post_process(self, retval):
        return self.retval

def register_magics(kernel):
    kernel.register_magics(KernelMagic)
