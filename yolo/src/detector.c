#include "network.h"
#include "region_layer.h"
#include "cost_layer.h"
#include "utils.h"
#include "parser.h"
#include "box.h"
#include "demo.h"
#include "option_list.h"
#include <io.h>
#include <conio.h>
#include <stdbool.h>


#ifndef _MAX_PATH
#define _MAX_PATH 260
#endif

#ifdef OPENCV
#include "opencv2/highgui/highgui_c.h"
#endif
static int coco_ids[] = { 1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,27,28,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,67,70,72,73,74,75,76,77,78,79,80,81,82,84,85,86,87,88,89,90 };

//void train_detector(char *datacfg, char *cfgfile, char *weightfile, int *gpus, int ngpus, int clear)
//{
//	list *options = read_data_cfg(datacfg);
//	char *train_images = option_find_str(options, "train", "data/train.list");
//	char *backup_directory = option_find_str(options, "backup", "/backup/");
//
//	srand(time(0));
//	char *base = basecfg(cfgfile);
//	printf("%s\n", base);
//	float avg_loss = -1;
//	network *nets = calloc(ngpus, sizeof(network));
//
//	srand(time(0));
//	int seed = rand();
//	int i;
//	for (i = 0; i < ngpus; ++i) {
//		srand(seed);
//#ifdef GPU
//		cuda_set_device(gpus[i]);
//#endif
//		nets[i] = parse_network_cfg(cfgfile);
//		if (weightfile) {
//			load_weights(&nets[i], weightfile);
//		}
//		if (clear) *nets[i].seen = 0;
//		nets[i].learning_rate *= ngpus;
//	}
//	srand(time(0));
//	network net = nets[0];
//
//	int imgs = net.batch * net.subdivisions * ngpus;
//	printf("Learning Rate: %g, Momentum: %g, Decay: %g\n", net.learning_rate, net.momentum, net.decay);
//	data train, buffer;
//
//	layer l = net.layers[net.n - 1];
//
//	int classes = l.classes;
//	float jitter = l.jitter;
//
//	list *plist = get_paths(train_images);
//	//int N = plist->size;
//	char **paths = (char **)list_to_array(plist);
//
//	load_args args = { 0 };
//	args.w = net.w;
//	args.h = net.h;
//	args.paths = paths;
//	args.n = imgs;
//	args.m = plist->size;
//	args.classes = classes;
//	args.jitter = jitter;
//	args.num_boxes = l.max_boxes;
//	args.d = &buffer;
//	args.type = DETECTION_DATA;
//	args.threads = 8;
//
//	args.angle = net.angle;
//	args.exposure = net.exposure;
//	args.saturation = net.saturation;
//	args.hue = net.hue;
//
//	pthread_t load_thread = load_data(args);
//	clock_t time;
//	int count = 0;
//	//while(i*imgs < N*120){
//	while (get_current_batch(net) < net.max_batches) {
//		if (l.random && count++ % 10 == 0) {
//			printf("Resizing\n");
//			int dim = (rand() % 10 + 10) * 32;
//			if (get_current_batch(net) + 100 > net.max_batches) dim = 544;
//			//int dim = (rand() % 4 + 16) * 32;
//			printf("%d\n", dim);
//			args.w = dim;
//			args.h = dim;
//
//			pthread_join(load_thread, 0);
//			train = buffer;
//			free_data(train);
//			load_thread = load_data(args);
//
//			for (i = 0; i < ngpus; ++i) {
//				resize_network(nets + i, dim, dim);
//			}
//			net = nets[0];
//		}
//		time = clock();
//		pthread_join(load_thread, 0);
//		train = buffer;
//		load_thread = load_data(args);
//
//		/*
//		int k;
//		for(k = 0; k < l.max_boxes; ++k){
//		box b = float_to_box(train.y.vals[10] + 1 + k*5);
//		if(!b.x) break;
//		printf("loaded: %f %f %f %f\n", b.x, b.y, b.w, b.h);
//		}
//		image im = float_to_image(448, 448, 3, train.X.vals[10]);
//		int k;
//		for(k = 0; k < l.max_boxes; ++k){
//		box b = float_to_box(train.y.vals[10] + 1 + k*5);
//		printf("%d %d %d %d\n", truth.x, truth.y, truth.w, truth.h);
//		draw_bbox(im, b, 8, 1,0,0);
//		}
//		save_image(im, "truth11");
//		*/
//
//		printf("Loaded: %lf seconds\n", sec(clock() - time));
//
//		time = clock();
//		float loss = 0;
//#ifdef GPU
//		if (ngpus == 1) {
//			loss = train_network(net, train);
//		}
//		else {
//			loss = train_networks(nets, ngpus, train, 4);
//		}
//#else
//		loss = train_network(net, train);
//#endif
//		if (avg_loss < 0) avg_loss = loss;
//		avg_loss = avg_loss*.9 + loss*.1;
//
//		i = get_current_batch(net);
//		printf("%d: %f, %f avg, %f rate, %lf seconds, %d images\n", get_current_batch(net), loss, avg_loss, get_current_rate(net), sec(clock() - time), i*imgs);
//		if (i % 1000 == 0 || (i < 1000 && i % 100 == 0)) {
//#ifdef GPU
//			if (ngpus != 1) sync_nets(nets, ngpus, 0);
//#endif
//			char buff[256];
//			sprintf(buff, "%s/%s_%d.weights", backup_directory, base, i);
//			save_weights(net, buff);
//		}
//		free_data(train);
//	}
//#ifdef GPU
//	if (ngpus != 1) sync_nets(nets, ngpus, 0);
//#endif
//	char buff[256];
//	sprintf(buff, "%s/%s_final.weights", backup_directory, base);
//	save_weights(net, buff);
//}


static int get_coco_image_id(char *filename)
{
	char *p = strrchr(filename, '_');
	return atoi(p + 1);
}

static void print_cocos(FILE *fp, char *image_path, box *boxes, float **probs, int num_boxes, int classes, int w, int h)
{
	int i, j;
	int image_id = get_coco_image_id(image_path);
	for (i = 0; i < num_boxes; ++i) {
		float xmin = boxes[i].x - boxes[i].w / 2.;
		float xmax = boxes[i].x + boxes[i].w / 2.;
		float ymin = boxes[i].y - boxes[i].h / 2.;
		float ymax = boxes[i].y + boxes[i].h / 2.;

		if (xmin < 0) xmin = 0;
		if (ymin < 0) ymin = 0;
		if (xmax > w) xmax = w;
		if (ymax > h) ymax = h;

		float bx = xmin;
		float by = ymin;
		float bw = xmax - xmin;
		float bh = ymax - ymin;

		for (j = 0; j < classes; ++j) {
			if (probs[i][j]) fprintf(fp, "{\"image_id\":%d, \"category_id\":%d, \"bbox\":[%f, %f, %f, %f], \"score\":%f},\n", image_id, coco_ids[j], bx, by, bw, bh, probs[i][j]);
		}
	}
}

void print_detector_detections(FILE **fps, char *id, box *boxes, float **probs, int total, int classes, int w, int h)
{
	int i, j;
	for (i = 0; i < total; ++i) {
		float xmin = boxes[i].x - boxes[i].w / 2.;
		float xmax = boxes[i].x + boxes[i].w / 2.;
		float ymin = boxes[i].y - boxes[i].h / 2.;
		float ymax = boxes[i].y + boxes[i].h / 2.;

		if (xmin < 0) xmin = 0;
		if (ymin < 0) ymin = 0;
		if (xmax > w) xmax = w;
		if (ymax > h) ymax = h;

		for (j = 0; j < classes; ++j) {
			if (probs[i][j]) fprintf(fps[j], "%s %f %f %f %f %f\n", id, probs[i][j],
				xmin, ymin, xmax, ymax);
		}
	}
}

void print_imagenet_detections(FILE *fp, int id, box *boxes, float **probs, int total, int classes, int w, int h)
{
	int i, j;
	for (i = 0; i < total; ++i) {
		float xmin = boxes[i].x - boxes[i].w / 2.;
		float xmax = boxes[i].x + boxes[i].w / 2.;
		float ymin = boxes[i].y - boxes[i].h / 2.;
		float ymax = boxes[i].y + boxes[i].h / 2.;

		if (xmin < 0) xmin = 0;
		if (ymin < 0) ymin = 0;
		if (xmax > w) xmax = w;
		if (ymax > h) ymax = h;

		for (j = 0; j < classes; ++j) {
			int class = j;
			if (probs[i][class]) fprintf(fp, "%d %d %f %f %f %f %f\n", id, j + 1, probs[i][class],
				xmin, ymin, xmax, ymax);
		}
	}
}

//void validate_detector(char *datacfg, char *cfgfile, char *weightfile)
//{
//	int j;
////	list *options = read_data_cfg(datacfg);
//	char *valid_images = option_find_str(options, "valid", "data/train.list");
//	char *name_list = option_find_str(options, "names", "data/names.list");
//	char *prefix = option_find_str(options, "results", "results");
//	char **names = get_labels(name_list);
//	char *mapf = option_find_str(options, "map", 0);
//	int *map = 0;
//	if (mapf) map = read_map(mapf);
//
//	network net = parse_network_cfg(cfgfile);
//	if (weightfile) {
//		load_weights(&net, weightfile);
//	}
//	set_batch_network(&net, 1);
//	fprintf(stderr, "Learning Rate: %g, Momentum: %g, Decay: %g\n", net.learning_rate, net.momentum, net.decay);
//	srand(time(0));
//
//	char *base = "comp4_det_test_";
//	list *plist = get_paths(valid_images);
//	char **paths = (char **)list_to_array(plist);
//
//	layer l = net.layers[net.n - 1];
//	int classes = l.classes;
//
//	char buff[1024];
//	char *type = option_find_str(options, "eval", "voc");
//	FILE *fp = 0;
//	FILE **fps = 0;
//	int coco = 0;
//	int imagenet = 0;
//	if (0 == strcmp(type, "coco")) {
//		snprintf(buff, 1024, "%s/coco_results.json", prefix);
//		fp = fopen(buff, "w");
//		fprintf(fp, "[\n");
//		coco = 1;
//	}
//	else if (0 == strcmp(type, "imagenet")) {
//		snprintf(buff, 1024, "%s/imagenet-detection.txt", prefix);
//		fp = fopen(buff, "w");
//		imagenet = 1;
//		classes = 200;
//	}
//	else {
//		fps = calloc(classes, sizeof(FILE *));
//		for (j = 0; j < classes; ++j) {
//			snprintf(buff, 1024, "%s/%s%s.txt", prefix, base, names[j]);
//			fps[j] = fopen(buff, "w");
//		}
//	}
//
//
//	box *boxes = calloc(l.w*l.h*l.n, sizeof(box));
//	float **probs = calloc(l.w*l.h*l.n, sizeof(float *));
//	for (j = 0; j < l.w*l.h*l.n; ++j) probs[j] = calloc(classes, sizeof(float *));
//
//	int m = plist->size;
//	int i = 0;
//	int t;
//
//	float thresh = .005;
//	float nms = .45;
//
//	int nthreads = 4;
//	image *val = calloc(nthreads, sizeof(image));
//	image *val_resized = calloc(nthreads, sizeof(image));
//	image *buf = calloc(nthreads, sizeof(image));
//	image *buf_resized = calloc(nthreads, sizeof(image));
//	pthread_t *thr = calloc(nthreads, sizeof(pthread_t));
//
//	load_args args = { 0 };
//	args.w = net.w;
//	args.h = net.h;
//	args.type = IMAGE_DATA;
//
//	for (t = 0; t < nthreads; ++t) {
//		args.path = paths[i + t];
//		args.im = &buf[t];
//		args.resized = &buf_resized[t];
//		thr[t] = load_data_in_thread(args);
//	}
//	time_t start = time(0);
//	for (i = nthreads; i < m + nthreads; i += nthreads) {
//		fprintf(stderr, "%d\n", i);
//		for (t = 0; t < nthreads && i + t - nthreads < m; ++t) {
//			pthread_join(thr[t], 0);
//			val[t] = buf[t];
//			val_resized[t] = buf_resized[t];
//		}
//		for (t = 0; t < nthreads && i + t < m; ++t) {
//			args.path = paths[i + t];
//			args.im = &buf[t];
//			args.resized = &buf_resized[t];
//			thr[t] = load_data_in_thread(args);
//		}
//		for (t = 0; t < nthreads && i + t - nthreads < m; ++t) {
//			char *path = paths[i + t - nthreads];
//			char *id = basecfg(path);
//			float *X = val_resized[t].data;
//			network_predict(net, X);
//			int w = val[t].w;
//			int h = val[t].h;
//			get_region_boxes(l, w, h, thresh, probs, boxes, 0, map);
//			if (nms) do_nms_sort(boxes, probs, l.w*l.h*l.n, classes, nms);
//			if (coco) {
//				print_cocos(fp, path, boxes, probs, l.w*l.h*l.n, classes, w, h);
//			}
//			else if (imagenet) {
//				print_imagenet_detections(fp, i + t - nthreads + 1, boxes, probs, l.w*l.h*l.n, classes, w, h);
//			}
//			else {
//				print_detector_detections(fps, id, boxes, probs, l.w*l.h*l.n, classes, w, h);
//			}
//			free(id);
//			free_image(val[t]);
//			free_image(val_resized[t]);
//		}
//	}
//	for (j = 0; j < classes; ++j) {
//		if (fps) fclose(fps[j]);
//	}
//	if (coco) {
//		fseek(fp, -2, SEEK_CUR);
//		fprintf(fp, "\n]\n");
//		fclose(fp);
//	}
//	fprintf(stderr, "Total Detection Time: %f Seconds\n", (double)(time(0) - start));
//}

void validate_detector_recall(char *cfgfile, char *weightfile)
{
	network net = parse_network_cfg(cfgfile);
	if (weightfile) {
		load_weights(&net, weightfile);
	}
	set_batch_network(&net, 1);
	fprintf(stderr, "Learning Rate: %g, Momentum: %g, Decay: %g\n", net.learning_rate, net.momentum, net.decay);
	srand(time(0));

	list *plist = get_paths("data/voc.2007.test");
	char **paths = (char **)list_to_array(plist);

	layer l = net.layers[net.n - 1];
	int classes = l.classes;

	int j, k;
	box *boxes = calloc(l.w*l.h*l.n, sizeof(box));
	float **probs = calloc(l.w*l.h*l.n, sizeof(float *));
	for (j = 0; j < l.w*l.h*l.n; ++j) probs[j] = calloc(classes, sizeof(float *));

	int m = plist->size;
	int i = 0;

	float thresh = .001;
	float iou_thresh = .5;
	float nms = .4;

	int total = 0;
	int correct = 0;
	int proposals = 0;
	float avg_iou = 0;

	for (i = 0; i < m; ++i) {
		char *path = paths[i];
		image orig = load_image_color(path, 0, 0);
		image sized = resize_image(orig, net.w, net.h);
		char *id = basecfg(path);
		network_predict(net, sized.data);
		get_region_boxes(l, 1, 1, thresh, probs, boxes, 1, 0);
		if (nms) do_nms(boxes, probs, l.w*l.h*l.n, 1, nms);

		char labelpath[4096];
		find_replace(path, "images", "labels", labelpath);
		find_replace(labelpath, "JPEGImages", "labels", labelpath);
		find_replace(labelpath, ".jpg", ".txt", labelpath);
		find_replace(labelpath, ".JPEG", ".txt", labelpath);

		int num_labels = 0;
		box_label *truth = read_boxes(labelpath, &num_labels);
		for (k = 0; k < l.w*l.h*l.n; ++k) {
			if (probs[k][0] > thresh) {
				++proposals;
			}
		}
		for (j = 0; j < num_labels; ++j) {
			++total;
			box t = { truth[j].x, truth[j].y, truth[j].w, truth[j].h };
			float best_iou = 0;
			for (k = 0; k < l.w*l.h*l.n; ++k) {
				float iou = box_iou(boxes[k], t);
				if (probs[k][0] > thresh && iou > best_iou) {
					best_iou = iou;
				}
			}
			avg_iou += best_iou;
			if (best_iou > iou_thresh) {
				++correct;
			}
		}

		fprintf(stderr, "%5d %5d %5d\tRPs/Img: %.2f\tIOU: %.2f%%\tRecall:%.2f%%\n", i, correct, total, (float)proposals / (i + 1), avg_iou * 100 / total, 100.*correct / total);
		free(id);
		free_image(orig);
		free_image(sized);
	}
}

//char* searchdir(char* filename)
//{
//	struct _finddata_t fd;
//	long handle;
//	int result = 1;
//
//	handle = _findfirst("../../../crawlingResult/*.jpg", &fd);  //현재 폴더 내 모든 파일을 찾는다.
//	char* path = "../../../crawlingResult/";
//
//	char* return_false = "no";
//	if (handle == -1)
//	{
//
//		strcpy(filename, return_false);
//		return filename;
//	}
//
//	while (result != -1)
//	{
//
//		//strcpy(fd_buffer, fd.name);
//		sprintf(filename, "%s%s\0", path, fd.name);
//
//		_findclose(handle);
//		/*free(fd_buffer);*/
//		return filename;
//	}
//}

char* searchdir(char* filename)
{
	struct _finddata_t fd;
	long handle;
	int result = 1;

	handle = _findfirst("crawlingResult/*.jpg", &fd);  //현재 폴더 내 모든 파일을 찾는다.
	char* path = "crawlingResult/";

	char* return_false = "no";
	if (handle == -1)
	{

		strcpy(filename, return_false);
		return filename;
	}

	while (result != -1)
	{

		//strcpy(fd_buffer, fd.name);
		sprintf(filename, "%s%s\0", path, fd.name);

		_findclose(handle);
		/*free(fd_buffer);*/
		return filename;
	}
}
void test_detector(char *datacfg, char *cfgfile, char *weightfile, float thresh, char *dataPath)
{
	list *options = read_data_cfg(datacfg, dataPath);
	char* namesPath = (char*)malloc(sizeof(char) * 200);
	sprintf(namesPath, "%s%s", dataPath, "names.list");
	char *name_list = option_find_str(options, "names", namesPath);
	char **names = get_labels(name_list);
	char *filename = (char*)malloc(sizeof(char) * 200);
	image **alphabet = load_alphabet();
	network net = parse_network_cfg(cfgfile);
	if (weightfile) {
		load_weights(&net, weightfile);
	}
	set_batch_network(&net, 1);
	srand(2222222);
	clock_t time;
	char buff[256];
	char *input = buff;
	int j;
	float nms = .4;
	while (1) {
		if (filename) {
			searchdir(filename);
			if (!strcmp(filename, "no")) {
				rmdir("crawlingResult");

				return;
			}
			strcpy(input, filename);


		}
		else {
			printf("Enter Image Path: ");
			fflush(stdout);
			input = fgets(input, 256, stdin);
			if (!input) return;
			strtok(input, "\n");
		}
		image im = load_image_color(input, 0, 0);
		image sized = resize_image(im, net.w, net.h);
		layer l = net.layers[net.n - 1];
		image im_result;

		box *boxes = calloc(l.w*l.h*l.n, sizeof(box));
		float **probs = calloc(l.w*l.h*l.n, sizeof(float *));
		for (j = 0; j < l.w*l.h*l.n; ++j) probs[j] = calloc(l.classes, sizeof(float *));

		float *X = sized.data;
		time = clock();
		network_predict(net, X);
		printf("%s: Predicted in %f seconds.\n", input, sec(clock() - time));
		get_region_boxes(l, 1, 1, thresh, probs, boxes, 0, 0);
		if (nms) do_nms_sort(boxes, probs, l.w*l.h*l.n, l.classes, nms);
		im_result = draw_detections(im, l.w*l.h*l.n, thresh, boxes, probs, names, alphabet, l.classes, input);
		//save_image(im, "predictions");
		//show_image(im, "predictions");

		printf("detect end\n");
		
		free_image(im);
		free_image(sized);
		free(boxes);
		free_ptrs((void **)probs, l.w*l.h*l.n);
#ifdef OPENCV
		/* cvWaitKey(0);
		cvDestroyAllWindows();*/
#endif
		remove(filename);

	}
}

void run_detector()
{
	char strBuffer[1000];
	
	getcwd(strBuffer, 1000);
	
	char datacfg[1000];
	char cfg[1000];
	char weights[1000];
	char dataPath[1000];
	sprintf(dataPath, "%s%s", strBuffer, "\\yolo\\build\\darknet\\x64\\data\\");
	sprintf(datacfg, "%s%s", strBuffer, "\\yolo\\build\\darknet\\x64\\data\\coco.data");

	printf("datacfg = %s\n", datacfg);
	sprintf(cfg, "%s%s", strBuffer, "\\yolo\\build\\darknet\\x64\\yolo.cfg");
	sprintf(weights, "%s%s", strBuffer, "\\yolo\\build\\darknet\\x64\\yolo.weights");
	test_detector(datacfg, cfg, weights, .24, dataPath);


}
