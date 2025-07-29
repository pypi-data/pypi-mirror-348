from typing import List, Dict, Any, Optional
import json

from ..envtype import EnvType
from .. import cmd
from ..config import Config

spack_root = "$prefix/share/spack"
spack_url = "https://github.com/spack/spack.git"
stutter = lambda x: f"{spack_root}/{x}/spack"
fix_csh_setenv = r"sed -n -e 's/^setenv \([^ ]*\) \(.*\);$/\1=''\2'';/p'"
spack_load = lambda x: "eval `{ %s load --csh %s | %s }" % (
                stutter("bin"), x, fix_csh_setenv)

setup_spack = [f"SPACK_ROOT = {spack_root}",
               "SPACK_USER_CACHE_PATH  = $SPACK_ROOT/.cache",
               "SPACK_USER_CONFIG_PATH = $SPACK_ROOT/.spack"]

#spack bootstrap now
#spack compiler find

#  specs: []
#  view: true
#  concretizer:
#    unify: true

class Spack(EnvType):
    #artifacts: [ "https://github.com/my_patch" ]
    #pre_configure: "git checkout deadbeef; patch -p1 <my_patch"
    pre_configure: Optional[str] = None
    spack: Dict[str,Any]

    def installScript(self, config: Config) -> cmd.Script:
        cmds = [ f"[ -d {spack_root} ] || git clone {spack_url} {spack_root}"
               ] + setup_spack
        if self.pre_configure is not None:
            cmds.append(self.pre_configure)
        cmds.append(f"{stutter('bin')} bootstrap now")

        # make an editable copy
        cfg = dict(self.spack)
        cfg['config'] = dict(cfg.get('config', {}))
        cfg['config']['install_tree'] = {'root': '$prefix/opt'}
        #cfg['config']['view'] = '$prefix' # had no effect when enabled!

        specfile = json.dumps({"spack":cfg}, indent=2)
        to_file = '>'
        for line in specfile.split('\n'):
            if len(line) == 0:
                continue
            cmds.append(f"echo {cmd.quote(line)} {to_file}{spack_root}/spackenv.yaml")
            to_file = '>>'
        #cmds.append(f"echo {cmd.quote(specfile)} >{spack_root}/spackenv.yaml")
        cmds.append(f"{stutter('bin')} env rm -f spackenv")
        cmds.append(f"{stutter('bin')} env create spackenv {spack_root}/spackenv.yaml")
        #cmds.append(f"{stutter('bin')} env activate spackenv")
        cmds.append(f"{stutter('bin')} -e spackenv install")

        cmds.append(f"{stutter('bin')} -e spackenv env view enable $prefix")
        # (create / enable view of this env.)
        # spack view -d true copy -i $prefix single-pkg@1.2
        # (single package)
        cmds.append(f"{stutter('bin')} clean -dms")

        #for spec in self.specs:
        #    cmds.append("{} install {}".format(
        #            stutter("bin"), cmd.quote(spec)))

        return cmd.run(*cmds)
    def loadScript(self, config: Config) -> cmd.Script:
        #cmds = [s for s in setup_spack]
        #for spec in self.specs:
        #    cmds.append(spack_load(cmd.quote(spec)))
        #return cmd.runonce(*cmds)
        return cmd.Script()
