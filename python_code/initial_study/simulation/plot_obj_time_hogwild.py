import numpy as np
from misc import utils
import matplotlib.pyplot as plt
import matplotlib
import os, re
import glob

def parseData(contents):
    lines = contents.split('\n')
    epoches, times, losses = [], [], []
    count = 0
    for l in lines:
        count += 1
        data = filter(None, l.split(' '))
        if count < 3 or len(data) != 3:
            continue
        epoches.append(int(data[0]))
        times.append(float(data[1]))
        losses.append(float(data[2]))
    return epoches, times, losses


if __name__ == '__main__':
    matplotlib.rcParams.update({'font.size': 30})
    ns = [1000, 2000, 5000]
    ds = [100, 200, 500]
    Ps = [1, 2, 4, 8]
    ss = [1.0]
    schemes = ['random', 'corr']
    linestyles = ['-', '--']
    nit = 100000
    for s in ss:
        filedir = os.path.join('..', 'results','simulations', 'Gaussian' + str(s), 'hogwild')
        for n in ns:
            for d in ds:
                for P in Ps:
                    fig = plt.figure(num=1, figsize=(20, 12))
                    ax = fig.add_subplot(1,1,1)

                    for i, (linestyle, scheme) in enumerate(zip(linestyles, schemes)):
                        filepattern = '%s_n%d_d%d_T%d_ths%d_gamma*' % (scheme, n, d, nit, P)
                        filepath = os.path.join(filedir, filepattern)
                        filepathc = glob.glob(filepath)
                        if len(filepathc) == 0:
                            raise Exception("File %s does not exist\n" % filepath)
                        # gammas, ys = [], []
                        for filepath in filepathc:
                            with open(filepath, 'r') as ins:
                                print('reading %s' % filepath)
                                contents = ins.read()
                            match = re.match(r'(.*)_gamma(.*)', filepath, re.M | re.I)
                            gamma = match.group(2)
                            # gammas.append(gamma)
                            epoches, times, losses = parseData(contents)
                            x = np.array(epoches)
                            y = np.log(np.array(losses))
                            # ys.append(y)
                        # ys = np.array(ys)
                        # yssum = np.sum(ys, axis=1)
                        # opt = np.argmin(yssum)
                            ax.plot(x, y, ls=linestyle, label='%s: step=%s' % (scheme, gamma), lw=2)

                    utils.set_axis(ax, xlabel='iterations', ylabel='log(loss)', xticks=None, yticks=None, xlim=None, fontsize=30)
                    plt.tight_layout()
                    savefile = 'n%d_d%d_T%d_ths%d.svg' % (n, d, nit, P)
                    save_dir = os.path.join(filedir, savefile)
                    fig.savefig(save_dir)
                    savefile = 'n%d_d%d_T%d_ths%d.pdf' % (n, d, nit, P)
                    save_dir = os.path.join(filedir, savefile)
                    fig.savefig(save_dir)
                    savefile = 'n%d_d%d_T%d_ths%d.jpg' % (n, d, nit, P)
                    save_dir = os.path.join(filedir, savefile)
                    fig.savefig(save_dir)
                    plt.cla()
                    print('succeed saving %s' % save_dir)
