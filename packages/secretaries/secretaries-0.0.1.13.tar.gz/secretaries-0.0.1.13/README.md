# Dependencies
Tested with:  
* [Python](https://www.python.org/) 3.9
* [Polars](https://github.com/pola-rs/polars) >= 0.19.2
* [Transformers](https://huggingface.co/docs/transformers/index) >= 4.33.1
* [Torch](https://github.com/pytorch/pytorch) >= 1.13.1
* [NLTK](https://www.nltk.org/) >= 3.8.1
* [importlib-resources](https://pypi.org/project/importlib-resources/) >= 6.1.0

# Installation


## From Github
```
pip3 install git+https://github.com/er1kb/secretaries
```
or clone and install locally:
```
git clone https://github.com/er1kb/secretaries.git && cd secretaries && pip3 install .
```

## From PyPI
```
python3 -m pip install secretaries
```


# English

## Purpose and motivations
This package is a three-pronged approach to finding and substituting personal data in text. It uses BERT models to search for named entities and regex to pin-point potential personal information. It summarizes counts of the tokens and entities found in the text. Although large language models might have the ability to do something like this, if you have sensitive and/or proprietary data, you probably do not want to shove it into some online cloud. The default model is the popular [David S. Lim's NER model](https://huggingface.co/dslim/bert-base-NER) at the Huggingface Hub. You can choose to run another one depending on your GPU resources and accuracy needs. 

In the English version, the base corpus is a mix of two online resources: a corpus of [7579 unique first names](https://www.cs.cmu.edu/Groups/AI/util/areas/nlp/corpora/names/) by Mark Kantrowitz and Github user craigh411's list of the [1000 most common American surnames](https://gist.github.com/craigh411/19a4479b289ae6c3f6edb95152214efc). It will be downloaded automatically the first time you run the code, assuming an Internet connection. For production use, you probably want to try and compile your own corpus from slightly more comprehensive sources. You can add to the corpus using the [input\_en/names](#names) folders and/or when calling the main function. 

Even though the model obfuscates names and such, it does not handle other information which may be unique to an individual. If someone writes their place of residence and their occupation, you might still be able to identify that person through text, even though their name has been removed. No computer model will ever completely absolve you of manual work, if required. The secrecy of people mentioned in your text is **your** responsibility. The model helps you obfuscate and summarize personal data but it makes no assumptions on the gravity of the context surrounding the task. 

## Instructions
### Data
You can feed the model a single string, a list of strings or a csv file. If supplying a csv, your data needs to have an id column of unique row ids and a text column.

BERT models have an upper limit of 512 tokens including punctuation. Longer texts will be split up for you into parts of at most 512 tokens, guided by punctuation so that sentences are preserved. The final (obfuscated) data is supplied as two versions: one split up by the max token length, and one concatenated into the original format. 

### 

### Input

To begin with, you can get good enough results by just running the NER part of the model, setting *corpus=False*. With domain specific data in a production setting, this might not be enough. The precision of the model will continue to improve if you help it by sorting words into the following three categories: words that are always names, words that are sometimes names and sometimes not (ambiguous), and finally words or phrases that you want to leave untouched (masks).

The first time you run the main function, a language specific input folder will be created in your working directory (ie where you are running the code), along with three subfolders. Each subfolder can contain any number of csv files. Each csv file contains a column named "token" and then has one token or phrase per row. If a subfolder contains multiple files, remember that all of these need to contain the "token" column in order to be combined when you run the model. 

#### Names
This is where you put words that are definitely names, irrespective of context. They will be added to the corpus search and replace (ie substitution by spelling), unless already present in the pre-loaded corpus. 

#### Ambiguous
Some words may or may not be names. Names that are ambiguous need to be inferred from the surrounding context, which is something that Named Entity Recognition does well. Consider the sentences "He is my best friend" and "His name is George Best". If "best" is hidden from the corpus search and replace, the first instance will be untouched, while the actual name in the second sentence will still be detected using NER.

If the corpus search returns a lot more names than the NER and you know you are using the right NER model, this indicates false positives. Go through output\_en/names\_corpus.csv, sort out the problematic words and put them in one or more csv files under input\_en/ambiguous/, then re-run the code. 

You will have to decide for yourself which words are ambiguous. A small starter kit will be loaded into the folder when it is created, for reference. 

#### Masks
You have the ability to mask tokens from the model. Masking tokens can consist of one or several words. These tokens will be hidden from the algorithm and then re-substituted at the end of the run. 

For example, adding "Big Ben" to the input\_en/maskings subfolder (of your working directory) ensures that this string stays untouched, while "Ben" not preceded by "Big " can still be treated as a name. Create a csv file in the maskings folder, where the first and only column is named "token" and each subsequent row is a masked token. 

If, like me, you work for a city, you might want to put all the names of streets and places into this folder. Streets are good candidates for masking because they often contain proper names that you might not want to remove, for example "Harris St." and "Coleman Rd.".

## Examples

### A single, short text
```
from secretaries import secretary as s
t = s.run("Bear Grylls once met a bear at Bear lake.", 
          lang = "English", 
          ambiguous = ["bear"],
          masks = ["Bear lake"],
          single_text_mode = True)
print(t)
```
```
[name] once met a bear at Bear lake.
```

### A longer text

This example runs the model on Jane Austen's *Pride and prejudice*. Time elapsed is about 12 minutes on a 24 core Threadripper CPU and an A4000 GPU. We set *corpus=False* to avoid getting a lot of false positives due to ambiguous words. 

```
import re
import urllib.request
url = r"https://www.gutenberg.org/cache/epub/1342/pg1342.txt" 
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
text = resp.read().decode('utf-8')

print('n characters: ' + str(len(text)))
print('n tokens: ' + str(len(re.split(r"\b", text))))

from secretaries import secretary as s
text = s.run(text = text, id_column = "id", text_column = "text", 
             model_name = "dslim/bert-large-NER",
             lang = "English", corpus = False,
             single_text_mode = True)
```

```
n characters: 763250
n tokens: 263829
```

```
> cat output_en/names_ner.csv
   1   │ token,count
   2   │ Elizabeth,338
   3   │ Darcy,287
   4   │ Jane,199
   5   │ Bennet,154
   6   │ Bingley,138
   7   │ Collins,131
   8   │ Lydia,123
   9   │ Wickham,104
  10   │ Catherine,74
  11   │ Gardiner,73
  12   │ Lizzy,63
  ...  │ ...
```

### A comma-separated text file (csv)

This example uses the default NER model. The data has an integer id column named "text\_number" and a text column aptly named "text". The unique ids are integers and specifying this helps with the final sorting of the data. The text has some unwanted html tags. 

```
from secretaries import secretary as s
d = s.run(csv = "my_data.csv", lang = "English",
          id_column = 'text_number', text_column = 'text', 
          remove_html = True, id_column_as_int = True)
```




# Other languages
Support for other languages could possibly be added. At minimum there needs to be a suitable model for Named Entity Recognition (NER) at the [Huggingface Model Hub](https://huggingface.co/models?pipeline_tag=text-classification&sort=trending&search=ner).


# Swedish

## Syfte och användningsområde
Sekreteraren är ett Python-paket för att flagga, ersätta och sammanfatta personuppgifter i löpande text. Den är en optimerad version av en tidigare kodbas som används av Malmö stad för att gallra personuppgifter i kundtjänstärenden. Det finns sannolikt andra modeller som tacklar samma problem, men detta är resultatet av våra överväganden och erfarenheter. Modellen vilar på [Kungliga Bibliotekets språkmodeller](https://github.com/Kungbib/swedish-bert-models) för NER (detektering av namngivna enheter i texten) och namnkorpuset från [Svensktext](https://github.com/peterdalle/svensktext). 

Modellen rensar personuppgifter med hög precision, men har ingen rutin för att identifiera utpekande information. Det är **ditt** ansvar att kontrollera texten med avseende på röjanderisk, det vill säga att kombinationen av olika uppgifter (inte) ger möjlighet att identifiera en eller flera nu levande individer. Modellen hjälper dig att rensa och sammanfatta personuppgifter, men den hjälper dig inte att bedöma situationens allvar. 

Namnen från [Svensktext](https://github.com/peterdalle/svensktext) laddas ner automatiskt till din arbetsmapp första gången du kör huvudfunktionen. Du kan göra tillägg till detta via undermappen [input\_se/namn](#namn).


## Instruktioner
### Data
Du kan mata in en enskild textsträng eller en lista med textsträngar: ["text1", "text2"]. För större datamängder med många texter vill du förmodligen mata in en csv-fil. Du behöver då ange namnen på en id-kolumn med unika id:n och en kolumn som innehåller texterna.  

BERT-modellen som används för att peka ut namngivna enheter i texten har en maxlängd på 512 ord inkl. skiljetecken. Längre texter kommer att delas upp i delar om max denna ordlängd, med hjälp av skiljetecken så att meningar inte delas upp. När skriptet har körts finns rensad data i två versioner: en uppdelad i max ordlängd och en sammanslagen till samma antal rader som den ursprungliga datamängden. 


### Övrig input (register)
Du kan öka modellens precision genom att sortera ord i tre kategorier: ord som alltid är namn, ord som kan vara namn eller inte (tveksamma), samt ord/fraser som ska bevaras i sin helhet (masker). Första gången du kör huvudfunktionen kommer en språkspecifik input-mapp med tre undermappar skapas i din arbetsmapp, det vill säga den mapp där du kör koden. Varje undermapp kan innehålla en eller flera csv-filer (kommaseparerad text). Varje csv-fil innehåller en kolumn med namnet "token" (utan citationstecken) och har sedan ett ord (alt. en fras) per rad. Om du har flera csv-filer i en undermapp, kom ihåg att samtliga måste ha kolumnen "token" namngiven i första raden, för att filerna ska kunna kombineras när du kör modellen. 

#### Namn
Här förvarar du ord som definitivt är namn, oavsett sammanhang. Dessa ord kommer att kombineras med namn-korpuset, såvida de inte redan finns där. Den svenska modellen bygger på ett mycket stort antal namn från [Svensktext](https://github.com/peterdalle/svensktext), men ovanliga namn sorteras bort för att undvika fel (false positives). Om din text innehåller ovanliga namn kan du behöva lägga till dessa, antingen via namn-mappen eller i kod när du anropar funktionen.

#### Tveksamma
Vissa ord är tvetydiga och kan vara namn eller inte, beroende på sammanhanget. Exempel är Stig, Björn, Lotta och Finn. Eftersom dessa namn ibland är meningsbärande ord kan vi inte rutinmässigt ta bort dem baserat på stavning. Om sammanhanget däremot indikerar att de utgör namn bör vi ta bort dem. Detta är poängen med att använda Named Entity Recognition (NER). 

Om sökningen med Svensktext uppenbart har flaggat fler namn än NER, lider din data av false positives, det vill säga ord som felaktigt flaggas som namn (givet att du har använt rätt NER-modell). Gå igenom csv-filen output\_se/namn\_korpus.csv, sortera uppenbara felaktigheter i en eller flera csv-filer under mappen input\_se/tveksamma och kör därefter skriptet på nytt. Det finns också en nedre brytpunkt i form av parametern min\_n\_persons = 100. Exempel: Enligt Svensktext finns 129 förekomster av namnet Snabb, som för-, efter- eller tilltalsnamn. Ordet finns därmed i korpuset, men du vill förmodligen inte slentrianmässigt flagga det som ett namn. När du på detta vis osynliggör ett namn för korpus-ersättningen, så kommer det fortfarande plockas upp av övriga delar av skriptet (NER och Regex) om sammanhanget indikerar att det är ett namn.

Första gången du kör huvudfunktionen sparas ett startkit med tveksamma ord under input\_se/tveksamma samtidigt som mapparna skapas. Vill du mot förmodan inte använda detta, ta bort filen men låt mappen vara kvar. 

#### Masker
Du kan maskera ord och fraser som inte ska ersättas. Exempelvis, i meningen "Gustav bor vid Gustav Adolfs torg" är bara den första förekomsten av "Gustav" en personuppgift. För att hålla resten av meningen intakt lägger du masken "Gustav Adolfs torg" i undermappen input\_se/maskeringar (under din arbetsmapp, där din kod körs). Om du jobbar inom en kommun så vill du förmodligen lägga in en lista på alla era gator och platser/besöksmål, för att hålla dessa intakta i texten. 

## Exempel

### En kort text
```
from secretaries import secretary as s
t = s.run(text = "Stig mötte Björn på en stig i skogen", 
          ambiguous = ["stig","björn"],
          single_text_mode = True)
print(t)
```
```
[namn] mötte [namn] på en stig i skogen
```


### En längre text
I det här exemplet laddar vi ner och analyserar Hjalmar Söderbergs *Förvillelser*. Det tar cirka 1,5 minut på en dator med 24-kärnors Threadripper CPU och en A4000 GPU. Till skillnad från motsvarande engelska exempel anger vi inte språk eller modell, eftersom svenska är standard och den mest omfattande BERT-modellen redan används.

```
import re
import urllib.request
url = r"https://www.gutenberg.org/cache/epub/30078/pg30078.txt" 
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
text = resp.read().decode('utf-8')
text = "\n".join(text.split("\n")[63:])

print('antal bokstäver: ' + str(len(text)))
print('antal ord/skiljetecken: ' + str(len(re.split(r"\b", text))))

from secretaries import secretary as s
text = s.run(text = text, id_column = "id", text_column = "text", 
                 single_text_mode = True, corpus = False)
                # sök inte med stavning (korpus), eftersom det blir många false positives
```

```
antal bokstäver: 256914
antal ord/skiljetecken: 85753

```

```
> cat output_se/namn_ner.csv
   1   │ token,count
   2   │ Tomas,105
   3   │ Märta,53
   4   │ Hall,29
   5   │ Ellen,26
   6   │ Greta,17
   7   │ Mortimer,14
   8   │ Arvidsons,7
   9   │ Weber,7
  10   │ Arvidson,7
  11   │ Gabel,6
  12   │ fru Wenschen,6
  13   │ Märta Brehm,5
  ...  │ ...
```

### En kommaseparerad textfil (csv)

Här läser vi in en csv-fil där kolumnen "text\_nummer" innehåller ett unikt id för varje text och kolumnen text innehåller själva texterna. Vi förtydligar också att id-kolumnen består av heltal, för sorteringens skull. Vi passar också på att radera html-taggar som smugit sin in i texten. 

```
from secretaries import secretary as s
d = s.run(csv = "min_data.csv", 
          id_column = 'text_nummer', text_column = 'text', 
          remove_html = True, id_column_as_int = True)
```


