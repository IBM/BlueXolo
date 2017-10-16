import pexpect

from pexpect import pxssh

class SshConnect():
    
    def CreateRobotFile(self, name, script):
        nombre = "Verify If Is Tape Attach"
        scrit = "{}\n\t[Arguments]   ${TARGET}   ${USERNAME}   ${PASSWORD}\n\tSSHLibrary.Open Connection     ${TARGET}\n\tSSHLibrary.Login      ${USERNAME}    ${PASSWORD}\n\t${output}=      SSHLibrary.Read     delay=1 s\n\tLog To Console      ${output}\n\t[Return]     ${output}\n\tSSHLibrary.Write      cat vpd.cfg|grep librarymodel\n".format(nombre)
        f = open("keyword.robot", "w")
        f.write("*** Keywords ***\n")
        f.write(scrit)
        f.close()

   def SendFile(self, filename, host, user, passwd):
        command = 'scp -o StrictHostKeyChecking=no {0} {1}@{2}:~/Desktop/Pruebas'.format(
            filename,
            user,
            host,
        )

       system = pexpect.spawn(command)
        system.expect('password:')
        system.sendline(passwd)
        system.expect('100%', timeout=600)

   def RunFie(self, filename,  host, user, passwd):

       ssh = pxssh.pxssh(timeout=10000)
        ssh.login(host, user, passwd)

conect = SshConnect()
#conect.SendFile("keyword.robot", "9.7.124.198", "tipadmin", "youRw3lcome")
conect.CreateRobotFile()