function Write-Network{
    param([String]$Network, [String]$InputExtension, [String]$OutputNetwork)
    Write-Output $Network
    # Create undirected reaction network
    python create_reaction_network.py `
-i  "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\fba_models\$Network.$InputExtension" `
-o  "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\reaction_networks\${OutputNetwork}_network.json" `
-f $InputExtension `
-v
    # Create directed reaction network
    python create_reaction_network.py `
-i  "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\fba_models\$Network.$InputExtension" `
-o  "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\reaction_networks\${OutputNetwork}_network_directed.json" `
-f $InputExtension `
-v `
-d `
-r
    # Create metabolite network
    python create_metabolite_network.py `
-i "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\fba_models\$Network.$InputExtension" `
-o "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\metabolite_networks\${OutputNetwork}_metabolite_network.json" `
-f $InputExtension `
-v
}

Write-Network iEK1008 xml iEk1008
Write-Network "iEK1011_2.0" json iEK1011_2_0
Write-Network iEK1011_deJesusEssen_media json iEK1011_deJesusEssen_media
Write-Network iEK1011_drugTesting_media json iEK1011_drugTesting_media
Write-Network iEK1011_griffinEssen_media json iEK1011_griffinEssen_media
Write-Network iEK1011_inVivo_media json iEK1011_inVivo_media
Write-Network iEK1011_m7H10_media json iEK1011_m7H10_media
Write-Network iNJ661 json iNJ661
Write-Network sMtb_BiGG_Identifiers json sMtb_BiGG
Write-Network "sMtb2.0" json sMtb_2_0
