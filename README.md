# UpdateRoyalties
Just a quick and dirty tool to update the royalties of specific NFTs of your collection to 97% (leave 3% buffer for marketplace fees (2% ME, 3% SA)).
Royalties will go to update authority wallet.

-Szenario: Scammer has stolen NFTs from a community member (wallet drained). Project leader with update authority to that collection can update the royalties to 97%
so that the scammer dont get any funds after selling on secondary market. Someone can just sweep the NFTs and give it back to the owner and gettin the funds from the update authority (Project leader needs to send it!).


# Install Libraries
pip install requests
pip install solana
pip install base58
pip install cryptography 


# How to

1.) There is a key.txt file.. export your private key to update authority from phantom (base58 format) and copy that to the key.txt file +save

2.) Install python libraries.. (see above)

3.) Open UpdateRoyalties.py -> see comment START CONFIG -> setup mints-array you want to update. -> save file -> run file!
