# edgecase_article

Edgecase article tool

Analogous to a crypto wallet transaction package. Articles are transactions on the Edgecase Datafeed blockchain.



### Requirements

- Python 3.x (developed with 3.5.2).

-- Note: Also runs under Python 2.x (developed with 2.7.12).

- Pytest 6.x (developed with 6.1.2).

- GPG 1.x, preferably 1.4.x (developed with 1.4.20).  
-- Required for creating or verifying signatures.

- Pip packages:  
-- colorlog (developed with 4.6.2). Required for colorised log output.

- The ```shasum``` tool. To produce SHA256 hashes, this tool uses the shell command ```shasum -a 256 <filepath>```.



### Installation

```
git clone --recurse-submodules git@github.com:sj-piano/edgecase_article.git
```

Now ```cd``` into the main directory, where you can run the tool ```cli.py```.

```
cd edgecase_article

python3 cli.py --help
```



### Tests


Note: ```cd``` into the main directory ```edgecase_article```, before running these commands.


Run all tests, including all tests within submodules:  
```pytest3 -q```


Run all tests for edgecase_article only:  
```pytest3 edgecase_article/test```


Run tests in a particular module:  
```pytest3 edgecase_article/test/test_verify.py```


Run specific test:  
```pytest3 edgecase_article/test/test_verify.py::test_verify_signed_datafeed_article_containing_checkpoint_article```


Run specific test with log output:  
```pytest3 -s --log-cli-level=INFO edgecase_article/test/test_verify.py::test_verify_signed_datafeed_article_containing_checkpoint_article```



### Notes

An article may be signed by its author.

A datafeed article can contain an article, a signed article, or a checkpoint article. A datafeed article is always signed by the Edgecase Datafeed key.

Python 2 is only used to run an additional SHA256 implementation, as a double-check for asset SHA256 hashes.




### Example: Validate the format of an article that you are writing.

```
python3 cli.py --task verify --articleFile ../new_articles/the_design_tree_of_a_blockchain.txt
```

Note: All option argument values can be indicated using an equals sign instead of a space.

Example:  
```
python3 cli.py --task=verify --articleFile=../new_articles/the_design_tree_of_a_blockchain.txt
```



### Example: Use logging.


```
python3 cli.py --task verify --articleFile ../new_articles/the_design_tree_of_a_blockchain.txt --logLevel info
```

```
stjohn@judgement:edgecase_article$ python3 cli.py --task verify --articleFile ../new_articles/the_design_tree_of_a_blockchain.txt --logLevel info
INFO     [edgecase_article.code.verify: 90 (verify)] File ../new_articles/the_design_tree_of_a_blockchain.txt contains a valid Element.
INFO     [edgecase_article.code.verify: 100 (verify)] Element name: article
```

Notes:  
- In the terminal, log output is colorised, if ```colorlog``` is installed.



### Example: Verify the content of the article (e.g. check that there are no unrecognised element names).

```
python3 cli.py --task verify --logLevel info --verifyContent --articleFile ../new_articles/the_design_tree_of_a_blockchain.txt
```

```
stjohn@judgement:edgecase_article$ python3 cli.py --task verify --logLevel info --verifyContent --articleFile ../new_articles/the_design_tree_of_a_blockchain.txt
INFO     [edgecase_article.code.verify: 90 (verify)] File ../new_article/the_design_tree_of_a_blockchain.txt contains a valid Element.
INFO     [edgecase_article.code.verify: 100 (verify)] Element name: article
INFO     [edgecase_article.code.verify: 170 (verify)] Content element: All descendant elements have permitted names.
INFO     [edgecase_article.code.verify: 192 (verify)] Content element: All descendant elements have been checked against the list of permitted tree structures.
```



### Example: Verify the filename of an article.

Note: Article filenames have a particular format on the Edgecase Datafeed blockchain.

```
python3 cli.py --task verify --logLevel info --verifyFileName --articleFile ../new_articles/the_design_tree_of_a_blockchain.txt
```

^ This produces an exception.

Expected formats:

- Checkpoint article:  
```checkpoint_0.txt```

- Article (whether or not signed by the author):  
```2017-08-19_stjohn_piano_lombard_street_by_walter_bagehot_chapter_1.txt```

- Datafeed article:  
```
2017-06-28_edgecase_datafeed_article_0_checkpoint_0.txt

2017-09-22_edgecase_datafeed_article_12_2017-09-22_stjohn_piano_warren_buffett_on_pensions.txt
```

```
python3 cli.py --task verify --logLevel info --verifyFileName --articleFile ../new_articles/2021-05-08_stjohn_piano_the_design_tree_of_a_blockchain.txt
```

^ This works.

Notes:  
- Each article has within itself a date, an author name, and a title. Datafeed articles have a second date, a datafeed name, and an article ID. When the filename is verified, the tool will check that all these items match the values in the filename. 



### Verify a signed datafeed article, which itself contains a signed article.

Note: For verifying signatures, you'll need a ```public_keys``` directory, which contains the necessary public key files. It can be named something other than ```public_keys```, if you want.

Example layout:
```
- work
-- datafeed_articles
-- edgecase_article
-- public_keys
--- edgecase_datafeed_public_key.txt
--- stjohn_piano_public_key.txt
```

```
python3 cli.py --task verify --logLevel info --verifyFileName --articleFile ../datafeed_articles/2017-06-28_edgecase_datafeed_article_1_2017-06-28_stjohn_piano_viewpoint.txt --publicKeyDir ../public_keys --verifySignature
```

Note:
- Any or all of the --verifyX options can be used in a single command.

```
stjohn@judgement:edgecase_article$ python3 cli.py --task verify --logLevel info --verifyFileName --articleFile ../datafeed_articles/2017-06-28_edgecase_datafeed_article_1_2017-06-28_stjohn_piano_viewpoint.txt --publicKeyDir ../public_keys --verifySignature
INFO     [edgecase_article.code.verify: 90 (verify)] File ../datafeed_articles/2017-06-28_edgecase_datafeed_article_1_2017-06-28_stjohn_piano_viewpoint.txt contains a valid Element.
INFO     [edgecase_article.code.verify: 100 (verify)] Element name: signed_datafeed_article
INFO     [edgecase_article.code.verify: 120 (verify)] File name verified for SignedDatafeedArticle
INFO     [edgecase_article.submodules.stateless_gpg.stateless_gpg.code.stateless_gpg: 141 (verify_signature)] GPG signature verified.
INFO     [edgecase_article.submodules.stateless_gpg.stateless_gpg.code.stateless_gpg: 141 (verify_signature)] GPG signature verified.
INFO     [edgecase_article.code.verify: 138 (verify)] Signature verified for internal SignedArticle
INFO     [edgecase_article.code.verify: 143 (verify)] Signature verified for SignedDatafeedArticle
```



### Sign an article.

Note: For creating signatures, you'll need a ```private_keys``` directory, which contains the necessary private key files. It can be named something other than ```private_keys``` if you want. You will also need a ```public_keys``` directory, so that the signature can be verified immediately after its creation.

Example layout:
```
- work
-- datafeed_articles
-- edgecase_article
-- new_article
-- private_keys
--- stjohn_piano_private_key.txt
-- public_keys
--- edgecase_datafeed_public_key.txt
--- stjohn_piano_public_key.txt
```

Note: Internally, the ```sign``` function will call the ```verify``` function prior to signing.

```
python3 cli.py --task sign --articleFile ../new_articles/2021-05-08_stjohn_piano_the_design_tree_of_a_blockchain.txt --publicKeyDir=../public_keys --privateKeyDir=../private_keys
```

Note: By default, the signed article will be written to the default output directory ```cli_output```. It will have an extra extension ```.signed```. You can use the ```--outputDir``` option to change the output directory if you wish.

Example log output:
```
stjohn@judgement:edgecase_article$ python3 cli.py --task sign --articleFile ../new_articles/2021-05-08_stjohn_piano_the_design_tree_of_a_blockchain.txt --publicKeyDir=../public_keys --privateKeyDir=../private_keys --logLevel info
INFO     [edgecase_article.code.verify: 90 (verify)] File ../new_article/2021-05-08_stjohn_piano_the_design_tree_of_a_blockchain.txt contains a valid Element.
INFO     [edgecase_article.code.verify: 100 (verify)] Element name: article
INFO     [edgecase_article.code.verify: 120 (verify)] File name verified for Article
INFO     [edgecase_article.code.verify: 170 (verify)] Content element: All descendant elements have permitted names.
INFO     [edgecase_article.code.verify: 192 (verify)] Content element: All descendant elements have been checked against the list of permitted tree structures.
INFO     [edgecase_article.submodules.stateless_gpg.stateless_gpg.code.stateless_gpg: 92 (make_signature)] GPG signature created.
INFO     [edgecase_article.submodules.stateless_gpg.stateless_gpg.code.stateless_gpg: 141 (verify_signature)] GPG signature verified.
INFO     [cli: 339 (sign)] Signed article written to ../new_article/2021-05-08_stjohn_piano_the_design_tree_of_a_blockchain.txt.signed
```



### Verify the assets of an article.

Note: If no asset directory exists, and the article contains no asset links, the ```--verifyAssets``` option will have no effect.

Verifying assets means:  
- Checking that all assets in the asset directory appear in at least one asset link within the article.  
- Checking that all asset links in the article lead to an actual asset in the asset directory.  
- Checking that the hash value in each asset link is identical to the re-calculated hash of the relevant asset file.  

The assets directory can be either ```assets``` or (the article name minus the .txt extension). Only one of these can exist. The asset directory is assumed to be in the same directory as the article. You can set the asset directory path manually using the ```--assetDir``` option.

```
python3 cli.py --task verify --logLevel info --articleFile ../datafeed_articles/2021-03-11_edgecase_datafeed_article_211_2021-03-09_nicholas_piano_public_key_nicholas_piano.txt --verifyFileName --verifyAssets
```

```
stjohn@judgement:edgecase_article$ python3 cli.py --task verify --logLevel info --articleFile ../datafeed_articles/2021-03-11_edgecase_datafeed_article_211_2021-03-09_nicholas_piano_public_key_nicholas_piano.txt --verifyFileName --verifyAssets
INFO     [edgecase_article.code.verify: 90 (verify)] File ../datafeed_articles/2021-03-11_edgecase_datafeed_article_211_2021-03-09_nicholas_piano_public_key_nicholas_piano.txt contains a valid Element.
INFO     [edgecase_article.code.verify: 100 (verify)] Element name: signed_datafeed_article
INFO     [edgecase_article.code.verify: 120 (verify)] File name verified for SignedDatafeedArticle
INFO     [edgecase_article.code.verify: 240 (verify)] Assets: 1 asset links found in article, containing 1 unique filenames.
INFO     [edgecase_article.code.verify: 277 (verify)] Assets: 1 asset files found in asset directory ('../datafeed_articles/2021-03-11_edgecase_datafeed_article_211_2021-03-09_nicholas_piano_public_key_nicholas_piano').
INFO     [edgecase_article.code.verify: 300 (verify)] Assets: All assets are linked at least once from the article.
INFO     [edgecase_article.code.verify: 312 (verify)] Assets: All asset links map to an asset in the asset directory.
INFO     [edgecase_article.code.verify: 348 (verify)] Assets: For each asset, the sha256 value has been re-calculated. All links to this asset contain the expected sha256 value.
```



### Datafeed Links


Within an EML article, links are EML structures (rather than http strings).

edgecase_article contains options for generating these links. The result files will be written to the default output directory ```cli_output```. You can use the ```--outputDir``` option to change the output directory if you wish.


Example hypertext link (a link to a webpage):

```
<link>
<type>hyperlink</type>
<reference>http://www.json.org</reference>
<text>Click here to go to www.json.org</text>
</link>
```


Example article link (a link to another article):

```
<link>
<type>article</type>
<article_title>checkpoint_0</article_title>
<datafeed>edgecase</datafeed>
<datafeed_article_id>0</datafeed_article_id>
<text>checkpoint 0</text>
</link>
```


Example asset link (a link to an asset contained within this particular article):

```
<link>
<type>asset</type>
<filename>stjohn_piano_public_key.txt</filename>
<text>[Click here to download keyfile]</text>
<sha256>73ba4c82ced0198a361cbb693098f5d40c09c2455b8eb5753138c1c74126574f</sha256>
</link>
```


Example external asset link (a link to an asset contained by another article):

```
<link>
<type>asset_of_another_article</type>
<article_title>Algorithm:_Generate_an_arithmetic_checksum_tree_for_a_Bitcoin_private_key</article_title>
<datafeed>edgecase</datafeed>
<datafeed_article_id>196</datafeed_article_id>
<filename>hexadecimal_addition_table.jpg</filename>
<text>hexadecimal_addition_table.jpg</text>
<sha256>d06447eac5e2a822607bd2ab058b65131b10fb138ca3a4a37b5586de08edf557</sha256>
</link>
```



Example: Generate EML links for all hypertext strings found within the article.

```
python3 cli.py --logLevel=info --task links --articleFile new_articles/article.txt --linkType=hyperlink
```

By default, the output will be written to the file ```cli_output/generated_hyperlinks.txt```.



Example: Generate EML links for all asset files found in the asset directory.

```
python3 cli.py --logLevel=info --task links --articleFile new_articles/article.txt --linkType asset --assetDir=new_articles/assets
```

By default, the output will be written to the file ```cli_output/generated_asset_links.txt```.



Example: Search for article link placeholders and use them to look up the actual article links. The placeholders contain the article's URI title wrapped in square brackets after the string ```LINK:```. Spaces are optional.

```
python3 cli.py --logLevel=info --task links --articleFile new_articles/article.txt --linkType article --articleLinksFile=settings/datafeed_article_links.json
```

By default, the output will be written to the file ```cli_output/selected_datafeed_article_links.txt```.

Sample placeholders:  
```
[LINK: excerpts_from_leviathan_wakes_by_james_s_a_corey]
[LINK: discussion_crypto_messaging_apps ]
[LINK:contract_1]
```

The ```datafeed_article_links.json``` file will not contain links for the most recent articles. You can download an up-to-date version from an Edgecase Datafeed node.

Command:  
```
curl --silent edgecase.pro/api/v1/datafeed_links/articles > datafeed_article_links.json
```

You can also download a human-readable version.

Command:  
```
curl --silent edgecase.pro/api/v1/datafeed_links/articles/data > datafeed_article_links.txt
```




Example: Search for external asset link placeholders and use them to look up the actual external asset links. The placeholders contain the asset's filename wrapped in square brackets after the string ```ASSET LINK:```. Spaces are optional.

```
python3 cli.py --logLevel=info --task links --articleFile new_articles/article.txt --linkType external_asset --assetLinksFile=settings/datafeed_asset_links.json
```

By default, the output will be written to the file ```cli_output/selected_datafeed_asset_links.txt```.

Sample placeholders:  
```
[ASSET LINK: contract_1.txt]
[ ASSET LINK : the_eye_of_argon_by_jim_theis.pdf]
```

The ```datafeed_asset_links.json``` file will not contain links for the most recent assets. You can download an up-to-date version from an Edgecase Datafeed node.

Command:  
```
curl --silent edgecase.pro/api/v1/datafeed_links/assets > datafeed_asset_links.json
```

You can also download a human-readable version.

Command:  
```
curl --silent edgecase.pro/api/v1/datafeed_links/assets/data > datafeed_asset_links.txt
```








