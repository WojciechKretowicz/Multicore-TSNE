class TraceTSNE:
    def __init__(self,
                 size=(25,17),
                 ffmpeg_command=None,
                 frame_rate=30,
                 resolution="1920x1080",
                 output_file="trace_tsne.mp4"):
	"""
	Class is used to make a video of iteration of gradient descent.

	size - tuple of length 2, describes the size of the each frame used in the video
	ffmpeg_command - if you want to directly specify how the video is made,
		it is a command line of ffmpeg, if you specify this, then the frame_rate
		and resolution is ignored
	frame_rate - frame rate of the video
	resolution - resolution of the video
	output_file - name of the output file
	"""

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
	"""
	This method makes a video from the given MulticoreTSNE object.

	TSNE - MulticoreTSNE object after fit method
	y - optional, the length must be equal to the number of points,
		used to colorize the points
	"""

        import seaborn as sns
        import os

        import matplotlib.pyplot as plt
        plt.rcParams['figure.figsize'] = self.size
	
	# making charts
        for i in range(TSNE.n_iter):
            plot = sns.scatterplot(TSNE.steps[i][:, 0],
                                   TSNE.steps[i][:, 1],
                                   hue=y, palette=sns.color_palette('bright'), legend=None)
            plot.set_title(str(i + 1), fontsize=30)
            plot.axis('off')
            plot = plot.get_figure()
            plot.savefig("tmp"+str(i + 1))
            plot.clf()

	# checking if the output file already exists
        if os.path.isfile(self.output_file):
            for i in range(TSNE.n_iter):
                os.remove("tmp" + str(i + 1) + ".png")
            raise Exception('Such file already exist!')
	
	# making a video from charts
        os.system(self.ffmpeg_command)
	
	# deleting charts
        for i in range(TSNE.n_iter):
            os.remove("tmp"+str(i + 1)+".png")