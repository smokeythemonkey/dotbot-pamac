import os, subprocess, dotbot, time

from enum import Enum

class PkgStatus(Enum):
    # Display these status names
    UP_TO_DATE = 'Your system is up-to-date.'
    INSTALLED= 'Transaction successfully finished.'
    UPDATED = 'Updated'
    NOT_FOUND = ''
    ERROR = 'Error'
    NOT_SURE = 'Could not determine'
    
class Pamac(dotbot.Plugin):
    _directive ='pamac'
    
    def __init__(self, context):
        super(Pamac, self).__init__(self)
        self._context = context
        self._strings = {}
        
        self._strings[PkgStatus.ERROR] = 'aborting'
        self._strings[PkgStatus.NOT_FOUND] = 'Could not find all packages'
        self._strings[PkgStatus.UPDATED] = 'Net Upgrade Size:'
        self._strings[PkgStatus.INSTALLED] = 'Total Installed Size:'
        self._strings[PkgStatus.UP_TO_DATE]='is up to date --skipping'
    
    def can_handle(self, directive):
        return directive == self._directive
    
    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('Pamac cannot handle directive %s' % directive)
        return self._process(data)
    
    def _process(self, packages):
        # defaults = self._context.defaults().get('pamac', {})
        results= {}
        successful=[PkgStatus.UP_TO_DATE, PkgStatus.UPDATED, PkgStatus.INSTALLED]
        
        if self._update() is True:
        
            for pkg in packages:
                if isinstance(pkg, dict):
                    self._log.error('Incorrect format')
                elif isinstance(pkg, list):
                    pass
                else:
                    pass
                result = self._install(pkg)
                results[pkg] = results.get(result, 0) + 1
                if result not in successful:
                    self._log.error(f"Could not install package '{pkg}'")
            
            if all([result in successful for result in results.keys()]):
                self._log.info('\nAll packages installed successfully')
                success = True
            else:
                success = False
                
            for status, amount in results.items():
                log = self._log.info if status in successful else self._log.error
                log('{} {}'.format(amount, status.value))

            return success
        else:
            self._log.warning('Could not determine what happened with system update')
        return PkgStatus.NOT_SURE

    def _install(self, pkg):
        """ """
        
        cmd ='LANG=en_US pamac --needed --no-confirm install {}'.format(pkg)        
        out = self._run_command(cmd, 'Installing \"{}\". Please wait...'.format(pkg))        
        
        for item in self._strings.keys():
            if out.decode('utf-8').find(self._strings[item]) >= 0:
                return item
            
        self._log.warning('Could not determine what happened with package {}'.format(pkg))
        return PkgStatus.NOT_SURE
    
    def _update(self):
        
        out = self._run_command('LANG=en_US pamac checkupdates', 'Checking for updates')
        if out.decode('utf-8').find(self._strings[PkgStatus.UP_TO_DATE]) <=0:
            out = self._run_command('LANG=en_US pamac update', 'Updating System, please wait...')
            if out.decode('utf-8').find(self._strings[PkgStatus.UPDATED]) >= 0:
                return True
            else:
                return False
            
    def _run_command(self, cmd, log_msg):
        
        self._log.info (log_msg)        
        time.sleep(2)
        
        proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out=proc.stdout.read()
        proc.stdout.close()
        
        return out
