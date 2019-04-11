class TraceTSNE:
    def __init__(self,
                 size=(25,17),
                 ffmpeg_command=None,
                 frame_rate=30,
                 resolution="1920x1080",
                 output_file="trace_tsne.mp4"):

        self.size = size
        self.ffmpeg_command = ffmpeg_command
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.output_file = output_file

        if ffmpeg_command == None:
            self.ffmpeg_command = "ffmpeg -r " + str(self.frame_rate) + \
                             " -f image2 -s " + self.resolution + \
                             " -i tmp%d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p " + \
                             output_file


    def transform(self, TSNE, y=None):

        import seaborn as sns
        import os

        import matplotlib.pyplot as plt
        plt.rcParams['figure.figsize'] = self.size

        for i in range(TSNE.n_iter):
            plot = sns.scatterplot(TSNE.steps[i][:, 0],
                                   TSNE.steps[i][:, 1],
                                   hue=y, palette=sns.color_palette('bright'), legend=None)
            plot.set_title(str(i + 1), fontsize=30)
            plot.axis('off')
            plot = plot.get_figure()
            plot.savefig("tmp"+str(i + 1))
            plot.clf()

        if os.path.isfile(self.output_file):
            for i in range(TSNE.n_iter):
                os.remove("tmp" + str(i + 1) + ".png")
            raise Exception('Such file already exist!')

        os.system(self.ffmpeg_command)

        for i in range(TSNE.n_iter):
            os.remove("tmp"+str(i + 1)+".png")