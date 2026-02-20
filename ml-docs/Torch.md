# Torch

Other languages:

- English
- [français](Torch_fr.md)

Outdated

**This page or section contains obsolete information and some statements may not be valid.** The technical documentation is currently being updated by our support team.

"[Torch](http://torch.ch/) is a scientific computing framework with wide support for machine learning algorithms that puts GPUs first. It is easy to use and efficient, thanks to an easy and fast scripting language, LuaJIT, and an underlying C/CUDA implementation."

Torch has a distant relationship to PyTorch.[1] PyTorch provides a [Python](Python.md) interface to software with similar functionality, but PyTorch is not dependent on Torch. See [PyTorch](PyTorch.md) for instructions on using it.

Torch depends on [CUDA](CUDA.md). In order to use Torch you must first load a CUDA module, like so:

```
[name@server ~]$ module load cuda torch

```

## Installing Lua packages

Torch comes with the Lua package manager, named [luarocks](https://luarocks.org/). Run

```
luarocks list

```

to see a list of installed packages.

If you need some package which does not appear on the list, use the following to install it in your own folder:

```
[name@server ~]$ luarocks install --local --deps-mode=all <package name>

```

If after this installation you are having trouble finding the packages at runtime, then add the following command[2] right before running "lua your\_program.lua"
command:

```
eval $(luarocks path --bin)

```

By experience, we often find packages that do not install well with luarocks. If you have a package that is not installed in the default module and need help installing it, please contact our [Technical support](Technical_Support.md).

1. ↑ See [https://stackoverflow.com/questions/44371560/what-is-the-relationship-between-pytorch-and-torch](https://stackoverflow.com/questions/44371560/what-is-the-relationship-between-pytorch-and-torch), [https://www.quora.com/What-are-the-differences-between-Torch-and-Pytorch](https://www.quora.com/What-are-the-differences-between-Torch-and-Pytorch), and [https://discuss.pytorch.org/t/torch-autograd-vs-pytorch-autograd/1671/4](https://discuss.pytorch.org/t/torch-autograd-vs-pytorch-autograd/1671/4) for some attempts to explain the connection.
2. ↑  [https://github.com/luarocks/luarocks/wiki/Using-LuaRocks#Rocks\_trees\_and\_the\_Lua\_libraries\_path](https://github.com/luarocks/luarocks/wiki/Using-LuaRocks#Rocks_trees_and_the_Lua_libraries_path)