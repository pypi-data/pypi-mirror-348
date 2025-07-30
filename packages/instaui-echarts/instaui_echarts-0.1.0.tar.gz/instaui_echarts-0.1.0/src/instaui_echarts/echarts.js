import { h, onMounted, shallowRef, watch } from "vue";
import * as echarts from 'echarts';


export default {
  props: ['option', 'theme', 'initOptions', 'resizeOption', 'updateOptions', 'chartEvents', 'zrEvents'],
  setup(props, { attrs, emit }) {
    const root = shallowRef();
    const chartIns = shallowRef();

    onMounted(() => {
      init(root, chartIns, props);
      autoResize(root, chartIns, props);

      setOption(root, chartIns, props);
      setChartEvents(root, chartIns, emit, props);
    })

    watch(() => props.option, (newVal, oldVal) => {

      setOption(root, chartIns, props);

    }, { deep: true })


    return () => {
      return h("div", { ...attrs, ref: root })
    };
  }

}


function init(root, chartIns, props) {
  if (!root.value) {
    return;
  }

  chartIns.value = echarts.init(
    root.value,
    props.theme,
    props.initOptions,
  )
}


function setOption(root, chartIns, props) {
  if (!chartIns.value) {
    init(root, chartIns, props);
  } else {
    chartIns.value.setOption(props.option || {}, props.updateOptions || {});
  }
}


function autoResize(root, chartIns, props) {

  watch(() => props.resizeOption, (resizeOption, _, onCleanup) => {

    let ro = null;

    if (resizeOption) {
      const { offsetWidth, offsetHeight } = root.value;
      const { throttle = 100 } = resizeOption;

      let isInitialResize = false;
      const callback = () => {
        chartIns.value.resize()
      }
      const resizeCallback = throttle ? echarts.throttle(callback, throttle) : callback;

      ro = new ResizeObserver(() => {

        if (!isInitialResize) {
          isInitialResize = true;
          if (
            root.value.offsetWidth === offsetWidth &&
            root.value.offsetHeight === offsetHeight
          ) {
            return;
          }
        }
        resizeCallback();
      })

      ro.observe(root.value);
    }

    onCleanup(() => {
      if (ro) {
        ro.disconnect();
        ro = null;
      }
    });

  }, { deep: true, immediate: true })

}


function setChartEvents(root, chartIns, emit, props) {

  const { chartEvents, zrEvents } = props;

  if (chartEvents) {
    chartEvents.forEach(event => {
      chartIns.value.on(event, (...args) => {
        if (args.length > 0) {
          const eventArgs = args[0]
          delete eventArgs['event']
          delete eventArgs['$vars']
        }

        emit(`chart:${event}`, ...args)
      });
    })
  }

  if (zrEvents) {
    zrEvents.forEach(event => {
      chartIns.value.getZr().on(event, (...args) => emit(`zr:${event}`, ...args));
    })
  }





}

