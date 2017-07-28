from rally import consts
from rally.task import scenario
from rally.plugins.openstack import scenario
from rally.plugins.openstack.scenarios.cinder import utils as cinder_utils
from rally.task import validation


@validation.add("required_services", services=[consts.Service.CINDER])
@validation.add("required_platform", platform="openstack", users=True)
@scenario.configure(context={"cleanup": ["cinder"]},
                    name="CinderWalt.create_and_delete_volumes",
                    platform="openstack")
class CreateAndDelete(cinder_utils.CinderBasic):
    def run(self, size, image=None, min_sleep=0, max_sleep=0, **kwargs):
        if image:
            kwargs["imageRef"] = image

        vol1 = self.cinder.create_volume(size, **kwargs)
        vol2 = self.cinder.create_volume(size, **kwargs)
        self.sleep_between(min_sleep, max_sleep)

        self.cinder.delete_volume(vol1)
        self.cinder.delete_volume(vol2)
