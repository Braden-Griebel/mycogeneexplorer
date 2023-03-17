# Function for writing all the centrality data for a single network
function Write-Data{
    param([String]$Network)
    Write-Output $Network
    # Create centrality dataframe for undirected reaction graph
    python .\create_centrality_dataframe.py `
-g "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\reaction_networks\${Network}_network.json" `
-o "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\network_data\$Network\${Network}_reaction_network" `
-f "both" `
-v
    # Create centrality dataframe for directed and weighted reaction graph
    python .\create_centrality_dataframe.py `
-g "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\reaction_networks\${Network}_network_directed.json" `
-o "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\network_data\$Network\${Network}_reaction_network_directed" `
-f "both" `
-v `
-w `
-d
    # Create centrality dataframe for directed but unweighted
    python .\create_centrality_dataframe.py `
-g "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\metabolite_networks\${Network}_metabolite_network.json" `
-o "C:\Users\brade\OneDrive\CGIDR Research\mycogeneexplorer\mycogeneexplorer\data\network_data\$Network\${Network}_metabolite_network" `
-f "both" `
-v `
-d
}

Write-Data iEK1008
Write-Data iEK1011_2_0
Write-data iNJ661
Write-Data sMtb_2_0
Write-Data sMtb_BiGG