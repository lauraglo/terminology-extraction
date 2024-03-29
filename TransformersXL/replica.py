import argparse
import sys
from typing import List

from flair.data import Corpus
from flair.data import Sentence
from flair.datasets import ColumnCorpus
from flair.datasets import DataLoader
from flair.embeddings import TokenEmbeddings, StackedEmbeddings, BertEmbeddings, ELMoEmbeddings, OpenAIGPTEmbeddings, \
    RoBERTaEmbeddings, XLMEmbeddings, XLNetEmbeddings, OpenAIGPT2Embeddings, TransformerWordEmbeddings


# FUNCTIONS

def bs(tokenizer,x,l,r,max_seq_len):
    if r>=l:
        mid = int(l + (r - l)/2)
        res=verifymid(tokenizer,x,mid,max_seq_len)
        if res==3:
            return mid
        elif res==2:
            return bs(tokenizer,x,mid+1,r,max_seq_len)
        else:
            return bs(tokenizer,x,l,mid-1,max_seq_len)

    else:
        print("wrong binary search")
        sys.exit()

def verifymid(tokenizer,x,mid,max_seq_len):
    limit=mid
    lw=x.to_tokenized_string().split(" ")
    lw=lw[:limit]
    sent=" ".join(lw)
    tokenized_text = tokenizer.tokenize(sent)
    if len(tokenized_text)>max_seq_len:
        return 1
    else:
        if verifymid_1(tokenizer,x,mid+1,max_seq_len)==True:
            return 2
        return 3


def verifymid_1(tokenizer,x,mid,max_seq_len):
    limit=mid
    lw=x.to_tokenized_string().split(" ")
    lw=lw[:limit]
    sent=" ".join(lw)
    tokenized_text = tokenizer.tokenize(sent)
    if len(tokenized_text)>max_seq_len:
        return False
    else:
        return True


def train(data_path, list_embedding, output, hyperparameter):

    # define columns
    columns = {0: 'text', 1: 'ner'}

    # print(args.no_dev)
    if args.no_dev==True:
        corpus: Corpus = ColumnCorpus(data_path, columns,
                                      train_file='Inspec/train.txt',
                                      test_file='Inspec/test.txt',
                                      #                               dev_file='dev.txt',
                                      in_memory=not args.not_in_memory
                                      )
    else:
        corpus: Corpus = ColumnCorpus(data_path, columns,
                                      train_file='Inspec/train.txt',
                                      test_file='Inspec/test.txt',
                                      dev_file='Inspec/dev.txt',
                                      in_memory=not args.not_in_memory
                                      )



    tag_type = 'ner'


    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
    print(tag_dictionary.idx2item)

    stats=corpus.obtain_statistics()
    print("Original\n",stats)

    if args.downsample_train>0:
        corpus.downsample(percentage = args.downsample_train, only_downsample_train = True)
        print("Train set downsampled by:",args.downsample_train)
        stats=corpus.obtain_statistics()
        print("Downsampled \n", stats)


    if args.embedding=="OpenAIGPT":
        print("Tokenizer",args.embedding)
        from pytorch_transformers import OpenAIGPTTokenizer

        if args.embedding_path!="":
            tokenizer = OpenAIGPTTokenizer.from_pretrained(args.embedding_path)
        else:
            tokenizer = OpenAIGPTTokenizer.from_pretrained("openai-gpt")

        max_seq_len=512
        print("taking max seq len as ",max_seq_len)

        new_train=[]
        for x in corpus.train:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_train.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)

                new_train.append(new_sent)


        new_test=[]
        for x in corpus.test:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_test.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_test.append(new_sent)

        new_dev=[]
        for x in corpus.dev:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_dev.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_dev.append(new_sent)

        corpus._train=new_train
        corpus._test=new_test
        corpus._dev=new_dev
        stats=corpus.obtain_statistics()
        print("Modified",stats)

    elif args.embedding=="Bert":
        print("Tokenizer",args.embedding)
        from pytorch_transformers import BertTokenizer
        if args.embedding_path!="":
            tokenizer = BertTokenizer.from_pretrained(args.embedding_path)
        else:
            tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

        max_seq_len=500
        print("taking max seq len as ",max_seq_len)


        new_train=[]
        for x in corpus.train:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_train.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_train.append(new_sent)


        new_test=[]
        for x in corpus.test:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_test.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_test.append(new_sent)


        new_dev=[]
        for x in corpus.dev:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_dev.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_dev.append(new_sent)



        corpus._train=new_train
        corpus._test=new_test
        corpus._dev=new_dev
        stats=corpus.obtain_statistics()
        print("Modified",stats)

    elif args.embedding=="XLM":
        print("Tokenizer",args.embedding)
        from pytorch_transformers import XLMTokenizer

        if args.embedding_path!="":
            tokenizer = XLMTokenizer.from_pretrained(args.embedding_path)
        else:
            tokenizer = XLMTokenizer.from_pretrained('xlm-mlm-en-2048')


        max_seq_len=500
        print("taking max seq len as ",max_seq_len)


        new_train=[]
        for x in corpus.train:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_train.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                for index in range(len(new_sent)):
                    new_sent[index].add_tag('ner', x[index].get_tag('ner').value)

                new_train.append(new_sent)

        new_test=[]
        for x in corpus.test:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_test.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                for index in range(len(new_sent)):
                    new_sent[index].add_tag('ner', x[index].get_tag('ner').value)

                new_test.append(new_sent)

        new_dev=[]
        for x in corpus.dev:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_dev.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                for index in range(len(new_sent)):
                    new_sent[index].add_tag('ner', x[index].get_tag('ner').value)

                new_dev.append(new_sent)


        corpus._train=new_train
        corpus._test=new_test
        corpus._dev=new_dev
        stats=corpus.obtain_statistics()
        print("Modified",stats)

    elif args.embedding=="RoBERTa":
        print("Tokenizer",args.embedding)

        from pytorch_transformers import BertTokenizer
        print("Using Bert tokenizer bert-base-uncased")
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        max_seq_len=500
        print("taking max seq len as ",max_seq_len)


        new_train=[]
        for x in corpus.train:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_train.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_train.append(new_sent)

        new_test=[]
        for x in corpus.test:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_test.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_test.append(new_sent)

        new_dev=[]
        for x in corpus.dev:

            tokenized_text = tokenizer.tokenize(x.to_plain_string())
            if len(tokenized_text)<=max_seq_len:
                new_dev.append(x)
            else:

                limit=bs(tokenizer,x,1,max_seq_len,max_seq_len)

                lw=x.to_tokenized_string().split(" ")
                lw=lw[:limit]

                sent=" ".join(lw)
                tokenized_text = tokenizer.tokenize(sent)
                if len(tokenized_text)>max_seq_len:
                    print("wrong binary search 1")
                    sys.exit()

                new_sent=Sentence(sent)
                new_dev.append(new_sent)


        corpus._train=new_train
        corpus._test=new_test
        corpus._dev=new_dev
        stats=corpus.obtain_statistics()
        print("Modified",stats)


        # Initialize embeddings
    embedding_types: List[TokenEmbeddings] = list_embedding

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    # Initialize sequence tagger
    from flair.models import SequenceTagger

    tagger: SequenceTagger = SequenceTagger(hidden_size=args.hidden_size,
                                            embeddings=embeddings,
                                            tag_dictionary=tag_dictionary,
                                            tag_type=tag_type,
                                            use_crf=args.use_crf,
                                            rnn_layers=args.rnn_layers,
                                            dropout=args.dropout, word_dropout=args.word_dropout, locked_dropout=args.locked_dropout
                                            )
    # Initialize trainer
    from flair.trainers import ModelTrainer

    trainer: ModelTrainer = ModelTrainer(tagger,
                                         corpus,
                                         #use_tensorboard=args.use_tensorboard
                                         )

    # Start training
    trainer.train(output,
                  learning_rate=args.lr,
                  mini_batch_size=args.batch_size,
                  anneal_factor=args.anneal_factor,
                  patience=args.patience,
                  max_epochs=args.num_epochs,
                  param_selection_mode=args.param_selection_mode,
                  num_workers=args.threads,

                  )
    return trainer


parser = argparse.ArgumentParser()

parser.add_argument('--embedding', type=str, default='TransformerXL', help='Bert ELMo ELMoTransformer TransformerXL OpenAIGPT')

parser.add_argument('--embedding_path', type=str, default='', help='transfo-xl-wt103 openai-gpt bert-large-cased')

parser.add_argument('--dataset_base_path', type=str, default='C:/Users/W10/PycharmProjects/terminology-extraction/', help='path to all the datasets in .txt format ')

parser.add_argument('--dataset', type=str, default='', help='name of the dataset in .txt format ')

parser.add_argument('--output_base_path', type=str, default='C:/Users/W10/PycharmProjects/terminology-extraction/', help='result path')

parser.add_argument('--iteration', type=str, default='', help='put iteration no (\'_#\' like \'_1\') if doing multiple runs')


parser.add_argument('--gpu', type=int, default=1, help='Please write which gpu to use 0 is for cuda:0 and so one \
                    if you want to use CPU specify -1 ')

parser.add_argument('--lr', type=float, default=0.05, help='learning rate ')

parser.add_argument('--anneal_factor', type=float, default=0.5, help='learning rate  annealing factor')

parser.add_argument('--patience', type=int, default=4, help='Patience is the number of epochs with no improvement the Trainer waits\
         until annealing the learning rate')

parser.add_argument('--batch_size', type=int, default=4, help=' batch size')
parser.add_argument('--num_epochs', type=int, default=60, help=' num of epochs')

parser.add_argument('--threads', type=int, default=12, help='no of threads for data loading')

parser.add_argument('--param_selection_mode', type=bool, default=False, help='put true if doing param selection')

parser.add_argument('--use_tensorboard', default=False, action='store_true')

parser.add_argument('--no_dev', default=False, action='store_true')

parser.add_argument('--use_crf', default=False, action='store_true')

parser.add_argument('--rnn_layers', type=int, default=1, help='')

parser.add_argument('--hidden_size', type=int, default=128, help='')

parser.add_argument('--dropout', type=float, default=0.0, help='')

parser.add_argument('--word_dropout', type=float, default=0.05, help='')

parser.add_argument('--locked_dropout', type=float, default=0.5, help='')

parser.add_argument('--downsample_train', type=float, default=0.0, help='Downsampling train primarily for KP20k ')

parser.add_argument('--not_in_memory',  default=False, action='store_true', help='If this argument used then the embeddings/datasets are read from the disc ')

#  python ake_algorithm.py --embedding TransformerXL --dataset Inspec --lr 0.05 --anneal_factor 0.5 --patience 4 --batch_size 4 --num_epochs 60 --threads 12 --is_dev True --use_crf True --rnn_layers 1 --hidden_size 128 --dropout 0.0 --word_dropout 0.05 --locked_dropout 0.5


args = parser.parse_args()


if args.embedding=='TransformerXL':
    if args.embedding_path!="":
        embedding=TransformerWordEmbeddings(args.embedding_path)
    else:
        embedding=TransformerWordEmbeddings()

if args.embedding=='Bert':
    if args.embedding_path!="":
        embedding=BertEmbeddings(args.embedding_path)
    else:
        embedding=BertEmbeddings()

if args.embedding=='ELMo':
    if args.embedding_path!="":
        embedding=ELMoEmbeddings(args.embedding_path)
    else:
        embedding=ELMoEmbeddings()

if args.embedding=='OpenAIGPT':
    if args.embedding_path!="":
        embedding=OpenAIGPTEmbeddings(args.embedding_path)
    else:
        embedding=OpenAIGPTEmbeddings()

if args.embedding=='OpenAI-GPT2':
    if args.embedding_path!="":
        embedding=OpenAIGPT2Embeddings(args.embedding_path)
    else:
        embedding=OpenAIGPT2Embeddings()

if args.embedding=='RoBERTa':
    if args.embedding_path!="":
        embedding=RoBERTaEmbeddings(args.embedding_path)
    else:
        embedding=RoBERTaEmbeddings()

if args.embedding=='XLM':
    if args.embedding_path!="":
        embedding=XLMEmbeddings(args.embedding_path)
    else:
        embedding=XLMEmbeddings()

if args.embedding=='XLNet':
    if args.embedding_path!="":
        embedding=XLNetEmbeddings(args.embedding_path)
    else:
        embedding=XLNetEmbeddings()



# Batch size learning rate anneal factor patience
output=args.output_base_path+args.embedding+"_"+args.embedding_path +"_"+args.dataset+args.iteration+"_downsample_train_"+str(args.downsample_train)+"_bs_"+str(args.batch_size)+ "_lr_"+str(args.lr)+ '_af_'+str(args.anneal_factor)+ '_p_'+ str(args.patience) + \
       "_hsize_"+str(args.hidden_size)+"_crf_"+str(int(args.use_crf))+"_lrnn_"+str(args.rnn_layers)+"_dp_"+str(args.dropout)+"_wdp_"+str(args.word_dropout)+"_ldp_"+str(args.locked_dropout)+"/"
dataset_path=args.dataset_base_path+args.dataset+"/"

print(output)
print(dataset_path)

print("\nHyper-Parameters\n")
arguments=vars(args)
for i in arguments:
    print('{0:25}  {1}'.format(i+":", str(arguments[i])))
    # print(i+" : "+str(arguments[i]))

trainer=train(dataset_path,[embedding],output,args)
print(args)

# Save both train and dev predictions
dev_eval_result, dev_loss = trainer.model.evaluate(
    DataLoader(
        trainer.corpus.dev,
        batch_size=args.batch_size,
        num_workers=args.threads,
    ),
    out_path=output+"dev.tsv",
    embeddings_storage_mode='none'
)

train_eval_result, train_loss = trainer.model.evaluate(
    DataLoader(
        trainer.corpus.train,
        batch_size=args.batch_size,
        num_workers=args.threads,
    ),
    out_path=output+"train.tsv",
    embeddings_storage_mode='none'
)
