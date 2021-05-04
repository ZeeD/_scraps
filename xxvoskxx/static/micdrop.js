'use strict';

const onload = () => {
	const ws = new WebSocket('ws://localhost:5000/ws/16000');

	ws.onmessage = (event) => {
		const data = event.data;
		const text = JSON.parse(data)['text'];
		document.querySelector('pre').textContent += text + '\n';
	};

	ws.onerror = console.error

	document.querySelector('#start').addEventListener('click', async () => {
		const microphone = await navigator.mediaDevices.getUserMedia({
			audio: {
				echoCancellation: true
			}
		});


		const recorder = RecordRTC(microphone, {
			type: 'audio',
			mimeType: 'audio/wav;codecs=pcm',
			recorderType: StereoAudioRecorder,
			timeSlice: 1000,
			ondataavailable: ws.send.bind(ws),
			desiredSampRate: 16000,
			numberOfAudioChannels: 1
		});

		recorder.startRecording();
	});
};

const main = () => {
	document.addEventListener('DOMContentLoaded', onload);
};

main();
