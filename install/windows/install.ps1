Import-Module BitsTransfer

# go to the temp dir
$location = Get-Location
Set-Location $HOME/AppData/Local/Temp/

# get current location
$curLocation = Get-Location

# installing anaconda
Write-Host 'fetching anaconda archieve' -ForegroundColor Green
$anacondaUrl = 'https://repo.continuum.io/archive/'
$anacondaWebPage = Invoke-WebRequest $anacondaUrl

Write-Host ' '
Write-Host 'analysing the HTML' -ForegroundColor Green
$anacondaHTML = $anacondaWebPage.parsedHTML
$archieves = $anacondaHTML.body.getElementsByTagName('TR')

foreach ($archieve in $archieves) {
    
    # extract information
    $dataItems = $archieve.children
    $binItem = $dataItems[0]
    $SizeItem = $dataItems[1]
    $timeItem = $dataItems[2]
    $hashItem = $dataItems[3]
    
    # see if the process is 64 bit
    if([Environment]::Is64BitProcess) {
        $nameRegex = 'Anaconda2-.*-Windows-x86_64.exe'
    }
    else {
        $nameRegex = 'Anaconda2-.*-Windows-x86.exe'
    }
    
    if($binItem.innerText -match $nameRegex){  # this is the latest version    
        # output infomation
        $name = $binItem.innerText
        $size = $SizeItem.innerText
        $time = $timeItem.innerText
        $hash = $hashItem.innerText
        Write-Host 'found the latest release of anaconda2'
        Write-Host "name of the file is: $name"
        Write-Host "the size of the file is: $size"
        Write-Host "the last modified time is: $time"
        Write-Host "the hase(MD5) is: $hash"
        
        # download the installer
        Write-Host ' '
        Write-Host 'downloading the anaconda2 installer' -ForegroundColor Green
        Write-Host 'this could takes a while' -ForegroundColor Green
        $fileUrl = "https://repo.continuum.io/archive/$name"
        Start-BitsTransfer $fileUrl ./anaconda_installer.exe -DisplayName 'Downloading the Latest Version of Anaconda2...'
        
        # check MD5
        Write-Host ' '
        Write-Host 'Checking MD5 value' -ForegroundColor Green
        $localHash = Get-FileHash ./anaconda_installer.exe -Algorithm MD5 
        if($localHash.Hash.ToUpper() = $hash.ToUpper()){
            Write-Host 'MD5 hash is good'
        }
        else {
            Write-Host 'The MD5 value is not the same, if you continue you maybe exposed to malware or virus' -ForegroundColor Red
            Write-Host 'Please check you network setting and try again. There maybe a proxy setted up' -ForegroundColor Red
            Read-Host 'Press Enter to continue, press Ctrl-C to stop'
        }
        
        # run the installer
        Write-Host ''
        Write-Host 'installing anaconda2, this should take a long time' -ForegroundColor Green
        Write-Host 'sorry we cannot display the process of installing' -ForegroundColor Green
        Write-Host 'Please sit back and relax' -ForegroundColor Green
        ./anaconda_installer.exe /AddToPath=0  /InstallationType=JustMe /S /D=$HOME\Anaconda2\ | Out-Null
        break
    }
}

# installing lexos
if(Test-Path 'C:\Lexos-master'){
    Write-Host ' '
    Write-Host 'you already have lexos installed'
    Write-Host 'run update.exe to update'
}
else {
    Write-Host ' '
    Write-Host 'downloading lexos' -ForegroundColor Green
    Write-Host 'This could take a while...' -ForegroundColor Green
    Write-Host 'Sorry we cannot display the status of the download, because it slows down the download' -ForegroundColor Green
    Write-Host 'Please sit back and relax' -ForegroundColor Green
    $lexosUrl = 'https://github.com/WheatonCS/Lexos/archive/master.zip'
    (new-object net.webclient).DownloadFile($lexosUrl, "$curLocation/master.zip")
    Write-Host ' '
    Write-Host 'extracting Lexos to C:\' -ForegroundColor Green
    Expand-Archive -Path "$curLocation\master.zip" -DestinationPath "C:\"
}


# installing requirements
Write-Host ' '
Write-Host 'installing other requirements (python modules)' -ForegroundColor Green
Invoke-Expression "$HOME\Anaconda2\Scripts\pip.exe install chardet"
Invoke-Expression "$HOME\Anaconda2\Scripts\pip.exe install gensim"
Invoke-Expression "$HOME\Anaconda2\Scripts\pip.exe install ete2"
Invoke-Expression "$HOME\Anaconda2\Scripts\pip.exe install natsort"

# creating desktop icon
Write-Host ' '
Write-Host 'creating desktop icon for you ^_^' -ForegroundColor Green
$shell = New-Object -ComObject WScript.Shell
$desktop = [System.Environment]::GetFolderPath('Desktop')
$shortcut = $shell.CreateShortcut("$desktop\Lexos.lnk")
$shortcut.TargetPath = "C:\Lexos-master\install\windows\run.cmd"
$shortcut.Save()

# go back 
Set-Location $location

# final message
Write-Host ' '
Write-Host 'lexos developer edition is successfully installed in "C:\Lexos-master"' -ForegroundColor Green
Write-Host 'if you want to uninstall lexos just remove that folder' -ForegroundColor Green
Write-Host 'thank you for using lexos.' -ForegroundColor Green
Read-Host 'press Enter to quit'

