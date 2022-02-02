function Find-Files($Path, $tClass)
{

    $i = 0x0

    [Reflection.Assembly]::LoadWithPartialName('System.IO.Compression.FileSystem')
    $outputDir = $Env:TMP + "\jar_output\"

    
    If(-not $(Test-Path $outputDir))
    {
        mkdir($outputDir)
    }

    $files = Get-ChildItem -ErrorAction SilentlyContinue -Path $Path -Recurse -Include *.jar

    $outputStr = "[+] JARs Found " + $files.Count
    Add-Content "log4j_vuln_upgrade.log" $outputStr

    ForEach($file in $files)
    {

        $i++

        ForEach($entry in ([IO.Compression.ZipFile]::OpenRead($file).Entries))
        {
            ForEach($cClass in $tClass)
            {
                if($entry | Select-String -Pattern $cClass -quiet)
                {
                    $outputStr = "[+] Found " + $entry + " on " + $file
                    Add-Content "log4j_vuln_upgrade.log" $outputStr

                    # TMP Folder jar
                    $Jarname =   $file | select BaseName
                    $folderJar = $outputDir + $Jarname.BaseName

                    If(-not $(Test-Path $folderJar))
                    {
                        mkdir($folderJar)
                    }

                    else
                    {
                        $folderJar = $folderJar + $i
                        mkdir($folderJar)
                    }

                    # TMP original folder 
                    $originalFolder = $folderJar + "\original\"
                    mkdir($originalFolder)

                    #Copy original jar
                    $finalFileName = $originalFolder + $Jarname.BaseName + ".zip"
                    Copy-Item $file -Destination  $finalFileName

                    # TMP mod folder
                    $mod = $folderJar + "\mod\"
                    mkdir($mod)

                    # TMP unzip folder
                    $unzipFolder = $mod + "\unzip\"
                    mkdir($unzipFolder)

                    # unzip jars
                    Expand-Archive -LiteralPath $finalFileName -DestinationPath $unzipFolder

                    # finding target class
                    $filesTarget  = Get-ChildItem -ErrorAction SilentlyContinue -Path $unzipFolder -Recurse -Include *$cClass

                    ForEach($cFileTarget in $filesTarget)
                    {
                        $outputStr = "[+] Deleting " + $cFileTarget
                        Add-Content "log4j_vuln_upgrade.log" $outputStr
                        Remove-Item $cFileTarget
                    }                    
                    
                    # TMP new_jar folder
                    $new_jar = $mod + "\new_jar\"
                    mkdir($new_jar)

                    $finalUpdatedZip = $new_jar + $Jarname.BaseName + ".zip"

                    $outputStr = "[+] Rebuilding zip from " + $unzipFolder + " to " + $finalUpdatedZip
                    Add-Content "log4j_vuln_upgrade.log" $outputStr

                    $uncompressFiles = $unzipFolder + "*"

                    Compress-Archive -Path $uncompressFiles -DestinationPath $finalUpdatedZip

                    $outputStr = "[+] Hot paching " + $finalUpdatedZip + " to " + $file
                    Add-Content "log4j_vuln_upgrade.log" $outputStr                    

                    # hot patching
                    Copy-Item $finalUpdatedZip -Destination $file
                }                
            }            
        }
    }
}

$targetClass = New-Object string[] 2
$targetClass[0] = "JMSAppender.class"
$targetClass[1] = "JndiLookup.class"

Find-Files "G:\\" $targetClass